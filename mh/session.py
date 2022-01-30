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
            "circle_id": None,
        }
        self.connection = connection_handler
        self.online_support_code = None
        self.pat_ticket = None
        self.capcom_id = ""
        self.hunter_name = ""
        self.hunter_stats = None
        self.layer = 0
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
        return pati.getDummyLayerData()

    def layer_end(self):
        self.layer = 0

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

    def leave_server(self):
        DB.leave_server(self)

    def get_gates(self):
        return DB.get_gates(self.local_info["server_id"])

    def join_gate(self, gate_id):
        DB.join_gate(self, self.local_info["server_id"], gate_id)

    def leave_gate(self):
        DB.leave_gate(self)

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

    def leave_city(self):
        DB.leave_city(self)

    def join_circle(self, circle_id):
        self.local_info['circle_id'] = circle_id

    def leave_circle(self):
        self.local_info['circle_id'] = None

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
        location = 1  # TODO: Don't hardcode location (city, quest, ...)
        hunter_rank, = struct.unpack_from(">H", self.hunter_info.data, 0)
        weapon_icon, = struct.unpack_from(">B", self.hunter_info.data, 0x10)
        weapon_icon -= 7  # Skip armor pieces and start at index zero
        return [
                (1, (weapon_icon << 24) | location),
                (2, hunter_rank << 16)
        ]
