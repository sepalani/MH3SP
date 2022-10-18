#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Monster Hunter database module.

    Monster Hunter 3 Server Project
    Copyright (C) 2021  Sepalani

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import random
import time

CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

MEDIA_VERSIONS = {
    "0903131810": "ROMJ08",
    "0906222136": "RMHJ08",
    "1001301045": "RMHE08",
    "1002121503": "RMHP08",
}

RESERVE_DC_TIMEOUT = 40.0


def new_random_str(length=6):
    return "".join(random.choice(CHARSET) for _ in range(length))


class ServerType(object):
    OPEN = 1
    ROOKIE = 2
    EXPERT = 3
    RECRUITING = 4


class LayerState(object):
    JOINABLE = 0
    EMPTY = 1
    FULL = 2


class Players(object):
    def __init__(self, capacity):
        assert capacity > 0, "Collection capacity can't be zero"

        self.slots = [None for _ in range(capacity)]
        self.used = 0

    def get_used_count(self):
        return self.used

    def get_capacity(self):
        return len(self.slots)

    def add(self, item):
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


class Circle(object):
    def __init__(self, parent):
        self.parent = parent
        self.leader = None
        self.players = Players(4)
        self.departed = False
        self.quest_id = 0
        self.embarked = False
        self.password = None
        self.remarks = None

        self.unk_byte_0x0e = 0

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

    def reset(self):
        self.leader = None
        self.players = Players(4)
        self.departed = False
        self.quest_id = 0
        self.embarked = False
        self.password = None
        self.remarks = None

        self.unk_byte_0x0e = 0


class City(object):
    LAYER_DEPTH = 3

    def __init__(self, name, parent):
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

    def get_population(self):
        return len(self.players)

    def in_quest_players(self):
        return sum(p.is_in_quest() for _, p in self.players)

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

    def get_pathname(self):
        pathname = self.name
        it = self.parent
        while it is not None:
            pathname = it.name + "\t" + pathname
            it = it.parent
        return pathname

    def get_first_empty_circle(self):
        for index, circle in enumerate(self.circles):
            if circle.is_empty():
                return circle, index
        return None, None

    def get_circle_for(self, leader_session):
        for index, circle in enumerate(self.circles):
            if circle.leader == leader_session:
                return circle, index
        return None, None

    def clear_circles(self):
        for circle in self.circles:
            circle.reset()

    def reserve(self, reserve):
        if reserve:
            self.reserved = time.time()
        else:
            self.reserved = None


class Gate(object):
    LAYER_DEPTH = 2

    def __init__(self, name, parent, city_count=40, player_capacity=100):
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


class Server(object):
    LAYER_DEPTH = 1

    def __init__(self, name, server_type, gate_count=40, capacity=2000,
                 addr=None, port=None):
        self.name = name
        self.parent = None
        self.server_type = server_type
        self.addr = addr
        self.port = port
        self.gates = [
            Gate("City Gate{}".format(i), self)
            for i in range(1, gate_count+1)
        ]
        self.players = Players(capacity)

    def get_population(self):
        return len(self.players) + sum((
            gate.get_population() for gate in self.gates
        ))

    def get_capacity(self):
        return self.players.get_capacity()


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


class TempDatabase(object):
    """A temporary database.

    TODO:
     - Finish the implementation
     - Make this thread-safe
    """

    def __init__(self):
        self.consoles = {
            # Online support code => Capcom IDs
        }
        self.sessions = {
            # PAT Ticket => Owner's session
        }
        self.capcom_ids = {
            # Capcom ID => Owner's session
            "C9I7D4": {"name": "Cid", "session": None},
            "D9R7K4": {"name": "Drakea", "session": None},
        }
        self.servers = new_servers()

    def get_support_code(self, session):
        """Get the online support code or create one."""
        support_code = session.online_support_code
        if support_code is None:
            while True:
                support_code = new_random_str(11)
                if support_code not in self.consoles:
                    session.online_support_code = support_code
                    break

        # Create some default users
        if support_code not in self.consoles:
            self.consoles[support_code] = [
                "C9I7D4", "D9R7K4", "******",
                "******", "******", "******"
            ]
        return support_code

    def new_pat_ticket(self, session):
        """Generates a new PAT ticket for the session."""
        while True:
            session.pat_ticket = new_random_str(11)
            if session.pat_ticket not in self.sessions:
                break
        self.sessions[session.pat_ticket] = session
        return session.pat_ticket

    def use_capcom_id(self, session, capcom_id, name=None):
        """Attach the session to the Capcom ID."""
        assert capcom_id in self.capcom_ids, "Capcom ID doesn't exist"

        not_in_use = self.capcom_ids[capcom_id]["session"] is None
        assert not_in_use, "Capcom ID is already in use"

        name = name or self.capcom_ids[capcom_id]["name"]
        self.capcom_ids[capcom_id] = {"name": name, "session": session}
        return name

    def use_user(self, session, index, name):
        """Use User from the slot or create one if empty"""
        assert 1 <= index <= 6, "Invalid Capcom ID slot"
        index -= 1
        users = self.consoles[session.online_support_code]
        while users[index] == "******":
            capcom_id = new_random_str(6)
            if capcom_id not in self.capcom_ids:
                self.capcom_ids[capcom_id] = {"name": name, "session": None}
                users[index] = capcom_id
                break
        else:
            capcom_id = users[index]
        name = self.use_capcom_id(session, capcom_id, name)
        session.capcom_id = capcom_id
        session.hunter_name = name

    def get_session(self, pat_ticket):
        """Returns existing PAT session or None."""
        session = self.sessions.get(pat_ticket)
        if session and session.capcom_id:
            self.use_capcom_id(session, session.capcom_id, session.hunter_name)
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

    def get_users(self, session, first_index, count):
        """Returns Capcom IDs tied to the session."""
        users = self.consoles[session.online_support_code]
        capcom_ids = [
            (i, (capcom_id, self.capcom_ids.get(capcom_id, {})))
            for i, capcom_id in enumerate(users[:count], first_index)
        ]
        size = len(capcom_ids)
        if size < count:
            capcom_ids.extend([
                (index, ("******", {}))
                for index in range(first_index+size, first_index+count)
            ])
        return capcom_ids

    def join_server(self, session, index):
        if session.local_info["server_id"] is not None:
            self.leave_server(session, session.local_info["server_id"])
        server = self.get_server(index)
        server.players.add(session)
        session.local_info["server_id"] = index
        session.local_info["server_name"] = server.name
        return server

    def leave_server(self, session, index):
        self.get_server(index).players.remove(session)
        session.local_info["server_id"] = None
        session.local_info["server_name"] = None

    def get_server_time(self):
        pass

    def get_game_time(self):
        pass

    def get_servers(self):
        return self.servers

    def get_server(self, index):
        assert 0 < index <= len(self.servers), "Invalid server index"
        return self.servers[index - 1]

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
        return users

    def create_city(self, session, server_id, gate_id, index,
                    settings, optional_fields):
        city = self.get_city(server_id, gate_id, index)
        city.optional_fields = optional_fields
        return city

    def join_city(self, session, server_id, gate_id, index):
        city = self.get_city(server_id, gate_id, index)
        city.parent.players.remove(session)
        city.players.add(session)
        session.local_info["city_id"] = index
        session.local_info["city_name"] = city.name
        return city

    def leave_city(self, session):
        city = self.get_city(session.local_info["server_id"],
                             session.local_info["gate_id"],
                             session.local_info["city_id"])
        city.parent.players.add(session)
        city.players.remove(session)
        if not city.get_population():
            city.clear_circles()
        session.local_info["city_id"] = None
        session.local_info["city_name"] = None

    def layer_detail_search(self, server_type, fields):
        cities = []

        def match_city(city, fields):
            return all((
                field in city.optional_fields
                for field in fields
            ))

        for server in self.servers:
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


CURRENT_DB = TempDatabase()


def get_instance():
    return CURRENT_DB
