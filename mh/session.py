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

import mh.database as db
import mh.pat_item as pati

from other.utils import to_bytearray, to_str

DB = db.get_instance()


class Session(object):
    """Server session class.

    TODO:
     - Finish the implementation
    """
    def __init__(self):
        """Create a session object."""
        self.local_info = {
            "server_id": None,
            "server_name": None,
            "gate_id": None,
            "gate_name": None,
            "city_id": None,
            "city_name": None
        }
        self.connection = None
        self.online_support_code = None
        self.pat_ticket = None
        self.capcom_id = ""
        self.hunter_name = ""
        self.hunter_stats = None
        self.layer = 0

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
        return DB.get_session(self)

    def get_support_code(self):
        """Return the online support code."""
        return DB.get_support_code(self)

    def delete(self):
        """Delete the current session from the database."""
        DB.del_session(self)

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

    def join_city(self, city_id):
        DB.join_city(self,
                     self.local_info["server_id"],
                     self.local_info["gate_id"],
                     city_id)

    def leave_city(self):
        DB.leave_city(self)
