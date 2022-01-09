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

CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

MEDIA_VERSIONS = {
    "0903131810": "ROMJ08",
    "0906222136": "RMHJ08",
    "1001301045": "RMHE08",
    "1002121503": "RMHP08",
}


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


class Players(list):
    """
    TODO: Probably use a better container or another approach.
    """
    def add(self, item):
        if item not in self:
            self.append(item)


class Circle(object):
    def __init__(self, parent):
        self.parent = parent
        self.leader = None
        self.players = Players()
        self.questId = 0
        self.embarked = False
        self.capacity = 4
        self.password = None
        self.remarks = None

    def get_population(self):
        return len(self.players)

    def get_capacity(self):
        return self.capacity

    def is_empty(self):
        return self.leader is None

    def has_password(self):
        return self.password is not None


class City(object):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.capacity = 4
        self.state = LayerState.EMPTY
        self.players = Players()
        self.optional_fields = []
        self.leader = None
        self.circles = [
            Circle(self) for _ in range(self.capacity)  # One circle per player
        ]

    def get_population(self):
        return len(self.players)

    def get_capacity(self):
        return self.capacity

    def get_state(self):
        size = self.get_population()
        if size == 0:
            return LayerState.EMPTY
        elif size < self.get_capacity():
            return LayerState.JOINABLE
        else:
            return LayerState.FULL

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


class Gate(object):
    def __init__(self, name, parent, city_count=40, player_capacity=100):
        self.name = name
        self.parent = parent
        self.state = LayerState.EMPTY
        self.capacity = player_capacity
        self.cities = [
            City("City{}".format(i), self)
            for i in range(1, city_count+1)
        ]
        self.players = Players()
        self.optional_fields = []

    def get_population(self):
        return len(self.players) + sum((
            city.get_population()
            for city in self.cities
        ))

    def get_capacity(self):
        return self.capacity

    def get_state(self):
        size = self.get_population()
        if size == 0:
            return LayerState.EMPTY
        elif size < self.get_capacity():
            return LayerState.JOINABLE
        else:
            return LayerState.FULL


class Server(object):
    def __init__(self, name, server_type, gate_count=40, capacity=2000,
                 addr=None, port=None):
        self.name = name
        self.server_type = server_type
        self.capacity = capacity
        self.addr = addr
        self.port = port
        self.gates = [
            Gate("City Gate{}".format(i), self)
            for i in range(1, gate_count+1)
        ]
        self.players = Players()

    def get_population(self):
        return len(self.players) + sum((
            gate.get_population() for gate in self.gates
        ))

    def get_capacity(self):
        return self.capacity


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

    def use_user(self, session, index, name):
        """Use Capcom ID from the slot or create one if empty"""
        assert 1 <= index <= 6, "Invalid Capcom ID slot"
        index -= 1
        users = self.consoles[session.online_support_code]
        while users[index] == "******":
            capcom_id = new_random_str(6)
            if capcom_id not in self.capcom_ids:
                users[index] = capcom_id
                break
        else:
            capcom_id = users[index]
            not_in_use = self.capcom_ids[capcom_id]["session"] is None
            assert not_in_use, "Capcom ID is already in use"
        name = name or self.capcom_ids[capcom_id]["name"]
        self.capcom_ids[capcom_id] = {"name": name, "session": session}
        session.capcom_id = capcom_id
        session.hunter_name = name

    def get_session(self, session):
        """Returns existing PAT session or the current one."""
        return self.sessions.get(session.pat_ticket, session)

    def del_session(self, session):
        """Delete the session from the database."""
        # TODO: Find a good place to purge old tickets
        """
        pat_ticket = session.pat_ticket
        if pat_ticket in self.sessions:
            del self.sessions[pat_ticket]
        """
        capcom_id = session.capcom_id
        if capcom_id in self.capcom_ids:
            self.capcom_ids[capcom_id]["session"] = None

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
        old_server = session.local_info["server_id"]
        if old_server is not None:
            self.leave_server(session, old_server)
        server = self.get_server(index)
        server.players.add(session)
        session.local_info["server_id"] = index
        return server

    def leave_server(self, session, index):
        self.get_server(index).players.remove(session)

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
        session.local_info["city_id"] = None
        session.local_info["city_name"] = None


CURRENT_DB = TempDatabase()


def get_instance():
    return CURRENT_DB
