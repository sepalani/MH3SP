#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Monster Hunter session module.

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

import struct

import mh.database as db
import mh.pat_item as pati

from other.utils import to_bytearray, to_str

DB = db.get_instance()


class SessionState:
    UNKNOWN = -1
    LOG_IN = 0
    GATE = 1
    CITY = 2
    CIRCLE = 3
    CIRCLE_STANDBY = 4
    QUEST = 5


class Session(object):
    """Server session class.

    TODO:
     - Finish the implementation
    """
    def __init__(self, connection_handler):
        """Create a session object."""
        self.local_info = {
            "server_id": None,
            "server_name": None,
            "gate_id": None,
            "gate_name": None,
            "city_id": None,
            "city_name": None,
            "city_size": 0,
            "city_capacity": 0,
            "circle_id": None,
        }
        self.connection = connection_handler
        self.online_support_code = None
        self.pat_ticket = None
        self.capcom_id = ""
        self.hunter_name = ""
        self.hunter_stats = None
        self.layer = 0
        self.state = SessionState.UNKNOWN
        self.binary_setting = b""
        self.search_payload = None
        self.hunter_info = pati.HunterSettings()

    def get(self, connection_data):
        """Return the session associated with the connection data, if any."""
        if hasattr(connection_data, "pat_ticket"):
            self.pat_ticket = to_str(
                pati.unpack_binary(connection_data.pat_ticket)
            )
        if hasattr(connection_data, "online_support_code"):
            self.online_support_code = to_str(
                pati.unpack_string(connection_data.online_support_code)
            )
        session = DB.get_session(self.pat_ticket) or self
        if session != self:
            assert session.connection is None, "Session is already in use"
            session.connection = self.connection
            self.connection = None
        return session

    def get_support_code(self):
        """Return the online support code."""
        return DB.get_support_code(self)

    def disconnect(self):
        """Disconnect the current session.

        It doesn't purge the session state nor its PAT ticket.
        """
        self.connection = None
        DB.disconnect_session(self)

    def delete(self):
        """Delete the current session.

        TODO:
         - Find a good place to purge old tickets.
         - We should probably create a SessionManager thread per server.
        """
        DB.delete_session(self)

    def is_jap(self):
        """TODO: Heuristic using the connection data to detect region."""
        pass

    def new_pat_ticket(self):
        DB.new_pat_ticket(self)
        return to_bytearray(self.pat_ticket)

    def get_users(self, first_index, count):
        return DB.get_users(self, first_index, count)

    def use_user(self, index, name):
        DB.use_user(self, index, name)

    def get_servers(self):
        return DB.get_servers()

    def get_server(self):
        assert self.local_info['server_id'] is not None
        return DB.get_server(self.local_info['server_id'])

    def get_gate(self):
        assert self.local_info['gate_id'] is not None
        return DB.get_gate(self.local_info['server_id'],
                           self.local_info['gate_id'])

    def get_city(self):
        assert self.local_info['city_id'] is not None
        return DB.get_city(self.local_info['server_id'],
                           self.local_info['gate_id'],
                           self.local_info['city_id'])

    def get_circle(self):
        assert self.local_info['circle_id'] is not None
        return self.get_city().circles[self.local_info['circle_id']]

    def layer_start(self):
        self.layer = 0
        self.state = SessionState.LOG_IN
        return pati.getDummyLayerData()

    def layer_end(self):
        if self.layer > 1:
            # City path
            self.leave_city()
        if self.layer > 0:
            # Gate path
            self.leave_gate()
            # Server path (executed at gate and higher)
            self.leave_server()
        self.layer = 0
        self.state = SessionState.UNKNOWN

    def layer_down(self, layer_id):
        if self.layer == 0:
            self.join_gate(layer_id)
        elif self.layer == 1:
            self.join_city(layer_id)
        else:
            assert False, "Can't go down a layer"
        self.layer += 1

    def layer_create(self, layer_id, settings, optional_fields):
        if self.layer == 1:
            city = self.create_city(layer_id, settings, optional_fields)
            city.leader = self
        else:
            assert False, "Can't create a layer from L{}".format(self.layer)
        self.layer_down(layer_id)

    def layer_up(self):
        if self.layer == 1:
            self.leave_gate()
        elif self.layer == 2:
            self.leave_city()
        else:
            assert False, "Can't go up a layer"
        self.layer -= 1

    def layer_detail_search(self, detailed_fields):
        server_type = self.get_server().server_type
        fields = [
            (field_id, value)
            for field_id, field_type, value in detailed_fields
        ]  # Convert detailed to simple optional fields
        return DB.layer_detail_search(server_type, fields)

    def join_server(self, server_id):
        return DB.join_server(self, server_id)

    def get_layer_children(self):
        if self.layer == 0:
            return self.get_gates()
        elif self.layer == 1:
            return self.get_cities()
        assert False, "Unsupported layer to get children"

    def get_layer_sibling(self):
        if self.layer == 1:
            return self.get_gates()
        elif self.layer == 2:
            return self.get_cities()
        assert False, "Unsupported layer to get sibling"

    def find_users_by_layer(self, server_id, gate_id, city_id,
                            first_index, count, recursive=False):
        if recursive:
            players = DB.get_all_users(server_id, gate_id, city_id)
        else:
            layer = \
                DB.get_city(server_id, gate_id, city_id) if city_id else \
                DB.get_gate(server_id, gate_id) if gate_id else \
                DB.get_server(server_id)
            players = list(layer.players)
        start = first_index - 1
        return players[start:start+count]

    def find_users(self, capcom_id, hunter_name, first_index, count):
        users = DB.find_users(capcom_id, hunter_name)
        start = first_index - 1
        return users[start:start+count]

    def leave_server(self):
        old_server = self.local_info["server_id"]
        if old_server is not None:
            self.local_info["server_id"] = None
            DB.leave_server(self, old_server)

    def get_gates(self):
        return DB.get_gates(self.local_info["server_id"])

    def join_gate(self, gate_id):
        DB.join_gate(self, self.local_info["server_id"], gate_id)
        self.state = SessionState.GATE

    def leave_gate(self):
        DB.leave_gate(self)
        self.state = SessionState.LOG_IN

    def get_cities(self):
        return DB.get_cities(self.local_info["server_id"],
                             self.local_info["gate_id"])

    def create_city(self, city_id, settings, optional_fields):
        return DB.create_city(self,
                              self.local_info["server_id"],
                              self.local_info["gate_id"],
                              city_id, settings, optional_fields)

    def join_city(self, city_id):
        DB.join_city(self,
                     self.local_info["server_id"],
                     self.local_info["gate_id"],
                     city_id)
        self.state = SessionState.CITY

    def leave_city(self):
        DB.leave_city(self)
        self.state = SessionState.GATE

    def try_transfer_city_leadership(self):
        if self.local_info['city_id'] is None:
            return None

        city = self.get_city()
        if city.leader != self:
            return None

        for _, player in city.players:
            if player == self:
                continue
            city.leader = player
            return player
        return None

    def join_circle(self, circle_id):
        # TODO: Move this to the database
        self.local_info['circle_id'] = circle_id
        self.state = SessionState.CIRCLE

    def set_circle_standby(self, val):
        assert self.state == SessionState.CIRCLE or \
            self.state == SessionState.CIRCLE_STANDBY or \
            self.state == SessionState.QUEST

        self.state = \
            SessionState.CIRCLE_STANDBY if val else SessionState.CIRCLE

    def is_circle_standby(self):
        return self.state == SessionState.CIRCLE_STANDBY

    def is_in_quest(self):
        return self.state == SessionState.QUEST

    def set_in_quest(self):
        self.state = SessionState.QUEST

    def leave_circle(self):
        # TODO: Move this to the database
        circle = self.get_circle()
        self.local_info['circle_id'] = None
        self.state = SessionState.CITY

        if circle.leader == self:
            circle.reset()
        else:
            circle.players.remove(self)

    def get_layer_players(self):
        if self.layer == 0:
            server = self.get_server()
            return server.players
        elif self.layer == 1:
            gate = self.get_gate()
            return gate.players
        elif self.layer == 2:
            city = self.get_city()
            return city.players
        else:
            assert False, "Can't find layer"

    def attempt_leave_all_layers(self, shutdown_type):
        assert 1 <= shutdown_type <= 2, "Invalid shutdown type"
        if shutdown_type != 1:
            return  # only shutdown_type 1 requires removal from layers
        if self.local_info["city_id"]:
            self.leave_city()
        if self.local_info["gate_id"]:
            self.leave_gate()
        if self.local_info["server_id"]:
            self.leave_server()

    def get_layer_host_data(self):
        """LayerUserInfo's layer_host."""
        return struct.pack("IIHHH",
                           3,  # layer depth?
                           self.local_info["server_id"] or 0,
                           1,  # ???
                           self.local_info["gate_id"] or 0,
                           self.local_info["city_id"] or 0)

    def get_optional_fields(self):
        """LayerUserInfo's optional fields."""
        location = int(self.is_in_quest())  # City - 0, Quest - 1
        hunter_rank = self.hunter_info.rank()
        weapon_type = self.hunter_info.weapon_type()
        return [
                (1, (weapon_type << 24) | location),
                (2, hunter_rank << 16)
        ]
