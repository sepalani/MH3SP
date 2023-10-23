#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2023 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Monster Hunter state module."""


from mh import database
from math import floor
import time
from threading import RLock, Event


try:
    # Python 3
    import selectors
except ImportError:
    # Python 2
    import externals.selectors2 as selectors


RESERVE_DC_TIMEOUT = 40.0


class ServerType(object):
    OPEN = 1
    ROOKIE = 2
    EXPERT = 3
    RECRUITING = 4


class LayerState(object):
    EMPTY = 1
    FULL = 2
    JOINABLE = 3


class Lockable(object):
    def __init__(self):
        self._lock = RLock()

    def lock(self):
        return self

    def __enter__(self):
        # Returns True if lock was acquired, False otherwise
        return self._lock.acquire()

    def __exit__(self, *args):
        self._lock.release()


class Players(Lockable):
    def __init__(self, capacity):
        assert capacity > 0, "Collection capacity can't be zero"

        self.slots = [None for _ in range(capacity)]
        self.used = 0
        super(Players, self).__init__()

    def get_used_count(self):
        return self.used

    def get_capacity(self):
        return len(self.slots)

    def add(self, item):
        with self.lock():
            if self.used >= len(self.slots):
                return -1

            item_index = self.index(item)
            if item_index != -1:
                return item_index

            for i, v in enumerate(self.slots):
                if v is not None:
                    continue

                self.slots[i] = item
                self.used += 1
                return i

            return -1

    def remove(self, item):
        assert item is not None, "Item != None"

        with self.lock():
            if self.used < 1:
                return False

            if isinstance(item, int):
                if item >= self.get_capacity():
                    return False

                self.slots[item] = None
                self.used -= 1
                return True

            for i, v in enumerate(self.slots):
                if v != item:
                    continue

                self.slots[i] = None
                self.used -= 1
                return True

            return False

    def index(self, item):
        assert item is not None, "Item != None"

        for i, v in enumerate(self.slots):
            if v == item:
                return i

        return -1

    def clear(self):
        with self.lock():
            for i in range(self.get_capacity()):
                self.slots[i] = None

    def find_first(self, **kwargs):
        if self.used < 1:
            return None

        for p in self.slots:
            if p is None:
                continue

            for k, v in kwargs.items():
                if getattr(p, k) != v:
                    break
            else:
                return p

        return None

    def find_by_capcom_id(self, capcom_id):
        return self.find_first(capcom_id=capcom_id)

    def __len__(self):
        return self.used

    def __iter__(self):
        if self.used < 1:
            raise StopIteration

        for i, v in enumerate(self.slots):
            if v is None:
                continue

            yield i, v

    def serialize(self):
        if self.used == 0:
            return {"capacity": len(self.slots)}
        pdict = {
            "slots": [(p.serialize() if p is not None else None)
                      for p in self.slots],
            "used": self.used
        }
        return pdict

    @staticmethod
    def deserialize(pdict, parent):
        if "used" not in pdict.keys():
            return Players(pdict["capacity"])
        from mh.session import Session
        players = Players(len(pdict["slots"]))
        players.slots = [(Session.deserialize(p) if p is not None else None)
                         for p in pdict["slots"]]
        players.used = pdict["used"]
        return players


class Circle(Lockable):
    def __init__(self, parent):
        # type: (City) -> None
        self.parent = parent
        self.leader = None
        self.players = Players(4)
        self.departed = False
        self.quest_id = 0
        self.embarked = False
        self.password = None
        self.remarks = None

        self.unk_byte_0x0e = 0
        super(Circle, self).__init__()

    def get_population(self):
        return len(self.players)

    def get_capacity(self):
        return self.players.get_capacity()

    def is_full(self):
        return self.get_population() == self.get_capacity()

    def is_empty(self):
        return self.leader is None

    def is_joinable(self):
        return not self.departed and not self.is_full()

    def has_password(self):
        return self.password is not None

    def reset_players(self, capacity):
        with self.lock():
            self.players = Players(capacity)

    def reset(self):
        with self.lock():
            self.leader = None
            self.reset_players(4)
            self.departed = False
            self.quest_id = 0
            self.embarked = False
            self.password = None
            self.remarks = None

            self.unk_byte_0x0e = 0

    def serialize(self):
        serialized_players = self.players.serialize()
        if "used" not in serialized_players.keys():
            return {}
        cdict = {
            "parent": None,
            "leader": self.leader.serialize() if self.leader is not None
            else None,
            "players": serialized_players,
            "departed": self.departed,
            "quest_id": self.quest_id,
            "embarked": self.embarked,
            "password": self.password,
            "remarks": self.remarks,
            "unk_byte_0x0e": self.unk_byte_0x0e
        }
        return cdict

    @staticmethod
    def deserialize(cdict, parent):
        if not len(cdict.keys()):
            return Circle(parent)
        from mh.session import Session
        circle = Circle(parent)
        circle.leader = Session.deserialize(cdict["leader"])\
            if cdict["leader"] is not None else None
        circle.players = Players.deserialize(cdict["players"], circle)
        circle.departed = cdict["departed"]
        circle.quest_id = cdict["quest_id"]
        circle.embarked = cdict["embarked"]
        circle.password = cdict["password"]
        circle.remarks = cdict["remarks"]
        circle.unk_byte_0x0e = cdict["unk_byte_0x0e"]
        return circle


class City(Lockable):
    LAYER_DEPTH = 3

    def __init__(self, name, parent):
        # type: (str, Gate) -> None
        self.name = name
        self.parent = parent
        self.state = LayerState.EMPTY
        self.players = Players(4)
        self.optional_fields = []
        self.leader = None
        self.reserved = None
        self.circles = [
            # One circle per player
            Circle(self) for _ in range(self.get_capacity())
        ]
        super(City, self).__init__()

    def get_population(self):
        return len(self.players)

    def in_quest_players(self):
        return sum(p.is_in_quest() for _, p in self.players)

    def get_capacity(self):
        return self.players.get_capacity()

    def get_state(self):
        if self.reserved:
            return LayerState.FULL
        size = self.get_population()
        if size == 0:
            return LayerState.EMPTY
        elif size < self.get_capacity():
            return LayerState.JOINABLE
        else:
            return LayerState.FULL

    def get_pathname(self):
        pathname = self.name
        it = self.parent
        while it is not None:
            pathname = it.name + "\t" + pathname
            it = it.parent
        return pathname

    def get_first_empty_circle(self):
        with self.lock():
            for index, circle in enumerate(self.circles):
                if circle.is_empty():
                    return circle, index
        return None, None

    def get_circle_for(self, leader_session):
        with self.lock():
            for index, circle in enumerate(self.circles):
                if circle.leader == leader_session:
                    return circle, index
        return None, None

    def clear_circles(self):
        with self.lock():
            for circle in self.circles:
                circle.reset()

    def reserve(self, reserve):
        with self.lock():
            if reserve:
                self.reserved = time.time()
            else:
                self.reserved = None

    def reset(self):
        with self.lock():
            self.state = LayerState.EMPTY
            self.players.clear()
            self.optional_fields = []
            self.leader = None
            self.reserved = None
            self.clear_circles()

    def get_all_players(self):
        with self.players.lock():
            return [p for _, p in self.players]

    def serialize(self):
        serialized_players = self.players.serialize()
        if "used" not in serialized_players.keys():
            return {"name": self.name}
        cdict = {
            "name": self.name,
            "parent": None,
            "state": self.state,
            "players": serialized_players,
            "optional_fields": self.optional_fields,
            "leader": self.leader.serialize() if self.leader is not None
            else None,
            "reserved": self.reserved,
            "circles": [c.serialize() for c in self.circles]
        }
        return cdict

    @staticmethod
    def deserialize(cdict, parent):
        if len(cdict.keys()) < 2:
            return City(cdict["name"], None)
        from mh.session import Session
        city = City(str(cdict["name"]) if cdict["name"] is not None
                    else cdict["name"], cdict["parent"])
        city.parent = parent
        city.state = cdict["state"]
        city.players = Players.deserialize(cdict["players"], parent)
        city.optional_fields = cdict["optional_fields"]
        city.leader = Session.deserialize(cdict["leader"])\
            if cdict["leader"] is not None else None
        city.reserved = cdict["reserved"]
        city.circles = [Circle.deserialize(c, city) for c in cdict["circles"]]
        return city


class Gate(object):
    LAYER_DEPTH = 2

    def __init__(self, name, parent, city_count=40, player_capacity=100):
        # type: (str, Server, int, int) -> None
        self.name = name
        self.parent = parent
        self.state = LayerState.EMPTY
        self.cities = [
            City("City{}".format(i), self)
            for i in range(1, city_count+1)
        ]
        self.players = Players(player_capacity)
        self.optional_fields = []

    def get_population(self):
        return len(self.players) + sum((
            city.get_population()
            for city in self.cities
        ))

    def get_capacity(self):
        return self.players.get_capacity()

    def get_state(self):
        size = self.get_population()
        if size == 0:
            return LayerState.EMPTY
        elif size < self.get_capacity():
            return LayerState.JOINABLE
        else:
            return LayerState.FULL

    def get_all_players(self):
        players = [p for _, p in self.players]
        for city in self.cities:
            players = players + city.get_all_players()
        return players

    def serialize(self):
        gdict = {
            "name": self.name,
            "parent": None,
            "state": self.state,
            "cities": [c.serialize() for c in self.cities],
            "players": self.players.serialize(),
            "optional_fields": self.optional_fields
        }
        return gdict

    @staticmethod
    def deserialize(gdict, parent):
        gate = Gate(str(gdict["name"]) if gdict["name"] is not None
                    else gdict["name"], parent)
        gate.state = gdict["state"]
        gate.cities = [City.deserialize(c, gate) for c in gdict["cities"]]
        gate.players = Players.deserialize(gdict["players"], gate)
        gate.optional_fields = gdict["optional_fields"]
        return gate


class Server(object):
    LAYER_DEPTH = 1

    def __init__(self, name, server_type, capacity=2000,
                 addr=None, port=None):
        self.name = name
        self.parent = None
        self.server_type = server_type
        self.addr = addr
        self.port = port
        gate_count = int(floor(capacity / 100))
        remainder = capacity % 100
        self.gates = [
            Gate("City Gate {}".format(i), self)
            for i in range(1, gate_count+1)
        ]
        if remainder:
            self.gates.append(Gate(
                "City Gate {}".format(len(self.gates)+1),
                self, player_capacity=remainder
            ))
        self.players = Players(capacity)

    def get_population(self):
        return len(self.players) + sum((
            gate.get_population() for gate in self.gates
        ))

    def get_capacity(self):
        return self.players.get_capacity()

    def get_all_players(self):
        players = [p for _, p in self.players]
        for gate in self.gates:
            players = players + gate.get_all_players()
        return players

    def serialize(self):
        sdict = {
            "name": self.name,
            "parent": self.parent,
            "server_type": self.server_type,
            "addr": self.addr,
            "port": self.port,
            "gates": [g.serialize() for g in self.gates],
            "players": self.players.serialize()
        }
        return sdict

    @staticmethod
    def deserialize(sdict):
        server = Server(str(sdict["name"]) if sdict["name"] is not None
                        else sdict["name"],
                        int(sdict["server_type"]) if sdict["server_type"]
                        else sdict["server_type"],
                        addr=str(sdict["addr"]) if sdict["addr"] is not None
                        else sdict["addr"],
                        port=int(sdict["port"]) if sdict["port"] is not None
                        else sdict["port"])
        server.parent = sdict["parent"]
        server.gates = [Gate.deserialize(g, server) for g in sdict["gates"]]
        server.players = Players.deserialize(sdict["players"], server)
        return server


def new_servers():
    servers = []
    servers.extend([
        Server("Valor{}".format(i), ServerType.OPEN)
        for i in range(1, 5)
    ])
    servers.extend([
        Server("Beginners{}".format(i), ServerType.ROOKIE)
        for i in range(1, 3)
    ])
    servers.extend([
        Server("Veterans{}".format(i), ServerType.EXPERT)
        for i in range(1, 3)
    ])
    servers.extend([
        Server("Greed{}".format(i), ServerType.RECRUITING)
        for i in range(1, 5)
    ])
    return servers


class State(object):
    def __init__(self):
        self.sessions = {
            # PAT Ticket => Owner's session
        }
        self.capcom_ids = {
            # Capcom ID => {Owner's name, Owner's session}
        }
        self.cache = None
        self.server_id = None
        self.server = None
        self.initialized = Event()

    def setup_server(self, server_id, server_name, server_type,
                     capacity, server_addr, server_port):
        self.server_id = server_id
        if server_id != 0:
            self.server = Server(server_name, server_type, capacity,
                                 addr=server_addr, port=server_port)
        else:
            self.server = None
        self.initialized.set()

    def new_pat_ticket(self, session):
        """Generates a new PAT ticket for the session."""
        while True:
            session.pat_ticket = database.new_random_str(11)
            if session.pat_ticket not in self.sessions:
                break
        self.sessions[session.pat_ticket] = session
        return session.pat_ticket

    def register_pat_ticket(self, session):
        """Register a Session's PAT ticket from another server."""
        self.sessions[session.pat_ticket] = session
        self.capcom_ids[session.capcom_id] = {"name": "", "session": None}
        self.join_server(session, self.server_id)

    def use_capcom_id(self, session, capcom_id, name=None):
        """Attach the session to the Capcom ID."""
        assert capcom_id in self.capcom_ids, "Capcom ID doesn't exist"

        not_in_use = self.capcom_ids[capcom_id]["session"] is None
        assert not_in_use, "Capcom ID is already in use. Try again in 60 seconds."

        name = name or self.capcom_ids[capcom_id]["name"]
        self.capcom_ids[capcom_id] = {"name": name, "session": session}

        db = database.get_instance()
        db.assign_name(capcom_id, name)

        # TODO: Check if stable index is required
        if capcom_id not in db.friend_lists:
            db.friend_lists[capcom_id] = []
        if capcom_id not in db.friend_requests:
            db.friend_requests[capcom_id] = []

        return name

    def use_user(self, session, index, name):
        """Use User from the slot or create one if empty"""
        assert 1 <= index <= 6, "Invalid Capcom ID slot"
        index -= 1
        users = database.get_instance().get_capcom_ids(
            session.online_support_code
        )
        while users[index] == "******":
            capcom_id = database.new_random_str(6)
            if capcom_id not in self.capcom_ids and \
                    not database.get_instance().get_name(capcom_id):
                self.capcom_ids[capcom_id] = {"name": name, "session": None}
                database.get_instance().assign_capcom_id(
                    session.online_support_code, index, capcom_id
                )
                break
        else:
            capcom_id = users[index]
        name = self.use_capcom_id(session, capcom_id, name)
        session.capcom_id = capcom_id
        session.hunter_name = name
        database.get_instance().use_user(session, index, name)

    def get_session(self, pat_ticket):
        """Returns existing PAT session or None."""
        session = self.sessions.get(pat_ticket)
        if session and session.capcom_id:
            try:
                self.use_capcom_id(
                    session, session.capcom_id, session.hunter_name
                )
            except AssertionError as e:
                return None
        return session

    def disconnect_session(self, session):
        """Detach the session from its Capcom ID."""
        if not session.capcom_id:
            # Capcom ID isn't chosen yet with OPN/LMP servers
            return
        self.capcom_ids[session.capcom_id]["session"] = None

    def delete_session(self, session):
        """Delete the session from the database."""
        self.disconnect_session(session)
        pat_ticket = session.pat_ticket
        if pat_ticket in self.sessions:
            del self.sessions[pat_ticket]
        self.cache.notify_session_deletion(session.capcom_id)

    def fetch_id(self, capcom_id):
        if capcom_id not in self.capcom_ids:
            self.capcom_ids[capcom_id] = {
                "name": database.get_instance().get_name(capcom_id),
                "session": None
            }
        return self.capcom_ids[capcom_id]

    def get_users(self, session, first_index, count):
        """Returns Capcom IDs tied to the session."""
        users = database.get_instance().get_capcom_ids(
            session.online_support_code
        )
        capcom_ids = [
            (i, (capcom_id, self.capcom_ids.get(
                                capcom_id, self.fetch_id(capcom_id)
                            )))
            for i, capcom_id in enumerate(users[:count], first_index)
        ]
        size = len(capcom_ids)
        if size < count:
            capcom_ids.extend([
                (index, ("******", {}))
                for index in range(first_index+size, first_index+count)
            ])
        return capcom_ids

    def join_server(self, session, server_id):
        server = self.get_server(server_id)
        if server_id != self.server_id:
            # Joining another server
            if self.cache:
                self.cache.send_session_info(server_id, session)
            if session.local_info["server_id"] is not None:
                self.leave_server(session)
        else:
            # Connecting to this server
            server.players.add(session)
        session.local_info["server_id"] = server_id
        session.local_info["server_name"] = server.name
        return server

    def leave_server(self, session):
        self.server.players.remove(session)
        session.local_info["server_id"] = None
        session.local_info["server_name"] = None

    def get_server_time(self):
        pass

    def get_game_time(self):
        pass

    def get_servers_version(self):
        return self.cache.servers_version

    def get_servers(self, include_ids=False):
        if not self.cache:
            return []
        server_ids, servers = self.cache.get_server_list(include_ids=True)
        below, above = [], []
        below_ids, above_ids = [], []
        for server_id, server in zip(server_ids, servers):
            if server_id < self.server_id:
                below.append(server)
                below_ids.append(server_id)
            elif server_id > self.server_id:
                above.append(server)
                above_ids.append(server_id)
        if self.server_id != 0:
            below.append(self.server)
            below_ids.append(self.server_id)
        below.extend(above)
        below_ids.extend(above_ids)
        if include_ids:
            return below_ids, below
        return below

    def get_server(self, server_id):
        if server_id == self.server_id:
            return self.server
        return self.cache.get_server(server_id)

    def get_gates(self, server_id):
        return self.get_server(server_id).gates

    def get_gate(self, server_id, index):
        gates = self.get_gates(server_id)
        assert 0 < index <= len(gates), "Invalid gate index"
        return gates[index - 1]

    def join_gate(self, session, server_id, index):
        gate = self.get_gate(server_id, index)
        gate.parent.players.remove(session)
        gate.players.add(session)
        session.local_info["gate_id"] = index
        session.local_info["gate_name"] = gate.name
        return gate

    def leave_gate(self, session):
        gate = self.get_gate(session.local_info["server_id"],
                             session.local_info["gate_id"])
        gate.parent.players.add(session)
        gate.players.remove(session)
        session.local_info["gate_id"] = None
        session.local_info["gate_name"] = None

    def get_cities(self, server_id, gate_id):
        return self.get_gate(server_id, gate_id).cities

    def get_city(self, server_id, gate_id, index):
        cities = self.get_cities(server_id, gate_id)
        assert 0 < index <= len(cities), "Invalid city index"
        return cities[index - 1]

    def reserve_city(self, server_id, gate_id, index, reserve):
        city = self.get_city(server_id, gate_id, index)
        with city.lock():
            reserved_time = city.reserved
            if reserve and reserved_time and \
               time.time()-reserved_time < RESERVE_DC_TIMEOUT:
                return False
            city.reserve(reserve)
        return True

    def get_all_users(self, server_id, gate_id, city_id):
        """Search for users in layers and its children.

        Let's assume wildcard search isn't possible for servers and gates.
        A wildcard search happens when the id is zero.
        """
        assert 0 < server_id, "Invalid server index"
        assert 0 < gate_id, "Invalid gate index"
        gate = self.get_gate(server_id, gate_id)
        users = list(gate.players)
        cities = [
            self.get_city(server_id, gate_id, city_id)
        ] if city_id else self.get_cities(server_id, gate_id)
        for city in cities:
            users.extend(list(city.players))
        return users

    def find_users(self, capcom_id="", hunter_name=""):
        assert capcom_id or hunter_name, "Search can't be empty"
        users = []
        for user_id, user_info in self.capcom_ids.items():
            session = user_info["session"]
            if not session:
                continue
            if capcom_id and capcom_id not in user_id:
                continue
            if hunter_name and \
                    hunter_name.lower() not in user_info["name"].lower():
                continue
            users.append(session)
        for user_info in self.cache.get_remote_players_list():
            if not user_info:
                continue
            if capcom_id and capcom_id not in user_info.capcom_id:
                continue
            if hunter_name and \
                    hunter_name.lower() not in user_info.hunter_name.lower():
                continue
            users.append(user_info)
        return users

    def create_city(self, session, server_id, gate_id, index,
                    settings, optional_fields):
        city = self.get_city(server_id, gate_id, index)
        with city.lock():
            city.optional_fields = optional_fields
            city.leader = session
            city.reserved = None
        return city

    def join_city(self, session, server_id, gate_id, index):
        city = self.get_city(server_id, gate_id, index)
        with city.lock():
            city.parent.players.remove(session)
            city.players.add(session)
            session.local_info["city_name"] = city.name
        session.local_info["city_id"] = index
        return city

    def leave_city(self, session):
        city = self.get_city(session.local_info["server_id"],
                             session.local_info["gate_id"],
                             session.local_info["city_id"])
        with city.lock():
            city.parent.players.add(session)
            city.players.remove(session)
            if not city.get_population():
                city.reset()
        session.local_info["city_id"] = None
        session.local_info["city_name"] = None

    def layer_detail_search(self, server_type, fields):
        cities = []

        def match_city(city, fields):
            with city.lock():
                return all((
                    field in city.optional_fields
                    for field in fields
                ))

        for server in self.get_servers():
            if server.server_type != server_type:
                continue
            for gate in server.gates:
                if not gate.get_population():
                    continue
                cities.extend([
                    city
                    for city in gate.cities
                    if match_city(city, fields)
                ])
        return cities

    def update_players(self):
        # Central server method for clearing unused Capcom IDs
        for capcom_id, player_info in self.capcom_ids.items():
            if player_info["session"] is not None and \
                    player_info["session"].local_info["server_id"] and \
                    capcom_id not in self.cache.players:
                self.capcom_ids[capcom_id]["session"] = None
            elif capcom_id in self.cache.players:
                self.capcom_ids[capcom_id]["session"] =\
                    self.cache.players[capcom_id]

    def update_capcom_id(self, session):
        # Central server method for keeping track of in-use Capcom IDs
        self.capcom_ids[session.capcom_id]["session"] = session

    def session_ready(self, pat_ticket):
        if self.server_id == 0:
            return True
        return self.cache.session_ready(pat_ticket)

    def set_session_ready(self, pat_ticket, store_data):
        self.cache.set_session_ready(pat_ticket, store_data)

    def close_cache(self):
        self.cache.close()


CURRENT_STATE = State()


def get_instance():
    return CURRENT_STATE
