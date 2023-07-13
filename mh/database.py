#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2021-2023 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Monster Hunter database module."""

import random
import sqlite3
import time
from threading import RLock, local as thread_local


CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

MEDIA_VERSIONS = {
    "0903131810": "ROMJ08",
    "0906222136": "RMHJ08",
    "1001301045": "RMHE08",
    "1002121503": "RMHP08",
}

BLANK_CAPCOM_ID = "******"

RESERVE_DC_TIMEOUT = 40.0


def new_random_str(length=6):
    return "".join(random.choice(CHARSET) for _ in range(length))


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
     - [Feature request] Send unread friend requests on next login
       * Imply saving the message info along the Capcom ID
    """

    def __init__(self):
        self.consoles = {
            # Online support code => Capcom IDs
        }
        self.sessions = {
            # PAT Ticket => Owner's session
        }
        self.capcom_ids = {
            # Capcom ID => Owner's name and session
        }
        self.friend_requests = {
            # Capcom ID => List of friend requests from Capcom IDs
        }
        self.friend_lists = {
            # Capcom ID => List of Capcom IDs
            # TODO: May need stable index, see Players class
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
            self.consoles[support_code] = [BLANK_CAPCOM_ID] * 6
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

        # TODO: Check if stable index is required
        if capcom_id not in self.friend_lists:
            self.friend_lists[capcom_id] = []
        if capcom_id not in self.friend_requests:
            self.friend_requests[capcom_id] = []

        return name

    def use_user(self, session, index, name):
        """Use User from the slot or create one if empty"""
        assert 1 <= index <= 6, "Invalid Capcom ID slot"
        index -= 1
        users = self.consoles[session.online_support_code]
        while users[index] == BLANK_CAPCOM_ID:
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
                (index, (BLANK_CAPCOM_ID, {}))
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
        return users

    def get_user_name(self, capcom_id):
        if capcom_id not in self.capcom_ids:
            return ""
        return self.capcom_ids[capcom_id]["name"]

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

    def add_friend_request(self, sender_id, recipient_id):
        # Friend invite can be sent to arbitrary Capcom ID
        if any(cid not in self.capcom_ids
               for cid in (sender_id, recipient_id)):
            return False
        if sender_id not in self.friend_requests[recipient_id]:
            self.friend_requests[recipient_id].append(sender_id)
        return True

    def accept_friend(self, capcom_id, friend_id, accepted):
        assert capcom_id in self.capcom_ids and friend_id in self.capcom_ids
        # Prevent duplicate if requests were sent both ways
        if accepted and friend_id not in self.friend_lists[capcom_id]:
            self.friend_lists[capcom_id].append(friend_id)
            self.friend_lists[friend_id].append(capcom_id)
        if capcom_id in self.friend_requests[friend_id]:
            self.friend_requests[friend_id].remove(capcom_id)
        if friend_id in self.friend_requests[capcom_id]:
            self.friend_requests[capcom_id].remove(friend_id)
        return True

    def delete_friend(self, capcom_id, friend_id):
        assert capcom_id in self.capcom_ids and friend_id in self.capcom_ids
        self.friend_lists[capcom_id].remove(friend_id)
        # TODO: find footage to see if it's removed in the other friend list
        #  i.e. self.friend_lists[friend_id].remove(capcom_id)
        #  AFAICT, there is no NtcFriendDelete packet
        return True

    def get_friends(self, capcom_id, first_index=None, count=None):
        assert capcom_id in self.capcom_ids
        begin = 0 if first_index is None else (first_index - 1)
        end = count if count is None else (begin + count)
        return [
            (k, self.capcom_ids[k]["name"])
            for k in self.friend_lists[capcom_id]
            if k in self.capcom_ids  # Skip unknown Capcom IDs
        ][begin:end]


class SafeSqliteConnection(object):
    """Safer SQLite connection wrapper."""

    def __init__(self, *args, **kwargs):
        self.__connection = sqlite3.connect(*args, **kwargs)
        self.__connection.row_factory = sqlite3.Row
        self.__connection.text_factory = str

    def __enter__(self):
        return self.__connection.__enter__()

    def __exit__(self, type, value, traceback):
        return self.__connection.__exit__(type, value, traceback)

    def __getattribute__(self, name):
        if name.startswith("_"):
            return object.__getattribute__(self, name)
        return self.__connection.__getattribute__(name)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            return object.__setattr__(self, name, value)
        return self.__connection.__setattr__(name, value)

    def __del__(self):
        self.__connection.close()


class ThreadSafeSqliteConnection(object):
    """Proxy object for thread local SQLite connection.

    SQLite connection/cursor can't be accessed nor closed from other threads.
    However, multiple threads can connect to the same file database.
    """
    def __init__(self, *args, **kwargs):
        self.__args = args
        self.__kwargs = kwargs
        self.__thread_ns = thread_local()
        self.__get_connection()

    def __enter__(self):
        return self.__get_connection().__enter__()

    def __exit__(self, type, value, traceback):
        return self.__get_connection().__exit__(type, value, traceback)

    def __getattribute__(self, name):
        if name.startswith("_"):
            return object.__getattribute__(self, name)
        return self.__get_connection().__getattribute__(name)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            return object.__setattr__(self, name, value)
        return self.__get_connection().__setattr__(name, value)

    def __get_connection(self):
        this = getattr(self.__thread_ns, "connection", None)
        if this is None:
            self.__thread_ns.connection = SafeSqliteConnection(*self.__args,
                                                               **self.__kwargs)
            this = self.__thread_ns.connection
        return this


class TempSQLiteDatabase(TempDatabase):
    """Hybrid SQLite/TempDatabase.

    The following data need to be retained after a shutdown:
     - Online support code and its Capcom IDs
     - Friend list per Capcom ID
     - Properties (at least the hunter name) per Capcom ID

    TODO:
     - Need proper documentation, especially for the overridable interface
    """

    DATABASE_NAME = "mh3sp.db"

    def __init__(self):
        self.parent = super(TempSQLiteDatabase, self)
        self.parent.__init__()
        self.connection = ThreadSafeSqliteConnection(self.DATABASE_NAME,
                                                     timeout=10.0)
        self.create_database()
        self.populate_database()

    def create_database(self):
        with self.connection as cursor:
            # Create consoles table
            #
            # TODO:
            #  - Should we add a "media_version" column to distinguish games?
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS consoles"
                " (support_code TEXT, slot_index INTEGER,"
                " capcom_id TEXT, name BLOB)"
            )
            cursor.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS profiles_uniq_idx"
                " ON consoles(support_code, slot_index)"
            )  # TODO: Fix support code generation to prevent race condition
            cursor.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS capcom_ids_uniq_idx"
                " ON consoles(capcom_id)"
            )  # TODO: Fix Capcom ID generation to prevent race condition

            # Create friend lists table
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS friend_lists"
                " (capcom_id TEXT, friend_id TEXT)"
            )
            cursor.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS friends_uniq_idx"
                " ON friend_lists(capcom_id, friend_id)"
            )

    def populate_database(self):
        with self.connection as cursor:
            rows = cursor.execute("SELECT * FROM consoles")
            for support_code, slot_index, capcom_id, name in rows:
                if support_code not in self.consoles:
                    self.consoles[support_code] = [BLANK_CAPCOM_ID] * 6
                self.consoles[support_code][slot_index - 1] = capcom_id
                self.capcom_ids[capcom_id] = {"name": name, "session": None}
                self.friend_lists[capcom_id] = []

            rows = cursor.execute("SELECT * FROM friend_lists")
            for capcom_id, friend_id in rows:
                self.friend_lists[capcom_id].append(friend_id)

    def force_update(self):
        """For debugging purpose."""
        with self.connection as cursor:
            for support_code, capcom_ids in self.consoles.items():
                for slot_index, capcom_id in enumerate(capcom_ids, 1):
                    info = self.capcom_ids.get(capcom_id, {"name": ""})
                    cursor.execute(
                        "INSERT OR IGNORE INTO consoles VALUES (?,?,?,?)",
                        (support_code, slot_index, capcom_id, info["name"])
                    )

            for capcom_id, friend_ids in self.friend_lists.items():
                for friend_id in friend_ids:
                    cursor.execute(
                       "INSERT OR IGNORE INTO friend_lists VALUES (?,?)",
                       (capcom_id, friend_id)
                    )

    def use_user(self, session, index, name):
        result = self.parent.use_user(session, index, name)
        with self.connection as cursor:
            cursor.execute(
                "INSERT OR REPLACE INTO consoles VALUES (?,?,?,?)",
                (session.online_support_code, index,
                 session.capcom_id, session.hunter_name)
            )
        return result

    def accept_friend(self, capcom_id, friend_id, accepted):
        if accepted:
            with self.connection as cursor:
                cursor.execute(
                    "INSERT INTO friend_lists VALUES (?,?)",
                    (capcom_id, friend_id)
                )
                cursor.execute(
                    "INSERT INTO friend_lists VALUES (?,?)",
                    (friend_id, capcom_id)
                )
        return self.parent.accept_friend(capcom_id, friend_id, accepted)

    def delete_friend(self, capcom_id, friend_id):
        with self.connection as cursor:
            cursor.execute(
                "DELETE FROM friend_lists"
                " WHERE capcom_id = ? AND friend_id = ?",
                (capcom_id, friend_id)
            )
        return self.parent.delete_friend(capcom_id, friend_id)


class DebugDatabase(TempSQLiteDatabase):
    """For testing purpose."""
    def __init__(self, *args, **kwargs):
        super(DebugDatabase, self).__init__(*args, **kwargs)

        CONSOLES = {
            # To use it, replace with a real support code
            "TEST_CONSOLE_1": [
                "AAAAAA", "BBBBBB", "CCCCCC", "DDDDDD", "EEEEEE", "FFFFFF"
            ],
            "TEST_CONSOLE_2": [
                "111111", "222222", "333333", "444444", "555555", "666666"
            ],
        }
        for key in CONSOLES:
            self.consoles.setdefault(key, CONSOLES[key])

        CAPCOM_IDS = {
            "AAAAAA": {"name": b"Hunt A", "session": None},
            "BBBBBB": {"name": b"Hunt B", "session": None},
            "CCCCCC": {"name": b"Hunt C", "session": None},
            "DDDDDD": {"name": b"Hunt D", "session": None},
            "EEEEEE": {"name": b"Hunt E", "session": None},
            "FFFFFF": {"name": b"Hunt F", "session": None},
            "111111": {"name": b"Hunt 1", "session": None},
            "222222": {"name": b"Hunt 2", "session": None},
            "333333": {"name": b"Hunt 3", "session": None},
            "444444": {"name": b"Hunt 4", "session": None},
            "555555": {"name": b"Hunt 5", "session": None},
            "666666": {"name": b"Hunt 6", "session": None},
        }
        for key in CAPCOM_IDS:
            self.capcom_ids.setdefault(key, CAPCOM_IDS[key])

        FRIEND_REQUESTS = {
            "AAAAAA": [],
            "BBBBBB": [],
            "CCCCCC": [],
            "DDDDDD": [],
            "EEEEEE": [],
            "FFFFFF": [],
            "111111": [],
            "222222": [],
            "333333": [],
            "444444": [],
            "555555": [],
            "666666": [],
        }
        for key in FRIEND_REQUESTS:
            self.friend_requests.setdefault(key, FRIEND_REQUESTS[key])

        FRIEND_LISTS = {
            "AAAAAA": [],
            "BBBBBB": [],
            "CCCCCC": [],
            "DDDDDD": [],
            "EEEEEE": [],
            "FFFFFF": [],
            "111111": [],
            "222222": [],
            "333333": [],
            "444444": [],
            "555555": [],
            "666666": [],
        }
        for key in FRIEND_LISTS:
            self.friend_lists.setdefault(key, FRIEND_LISTS[key])

        # Hack to force update the database with the debug data once
        if hasattr(self, "force_update"):
            self.force_update()


CURRENT_DB = TempSQLiteDatabase()


def get_instance():
    return CURRENT_DB
