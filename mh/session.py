#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2021-2023 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Monster Hunter session module."""

import struct
import time

import mh.database as db
from mh.state import get_instance, Players, LayerState
import mh.pat_item as pati

from other.utils import to_bytearray, to_str

DB = db.get_instance()
STATE = get_instance()


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
        self.request_reconnection = False
        self.pat_ticket = None
        self.capcom_id = ""
        self.hunter_name = b""
        self.hunter_stats = None
        self.layer = 0
        self.state = SessionState.UNKNOWN
        self.binary_setting = b""
        self.search_payload = None
        self.loaded_server_ids = {}
        self.hunter_info = pati.HunterSettings()

    def serialize(self):
        pdict = {
            "pat_ticket": self.pat_ticket,
            "local_info_server_id": self.local_info["server_id"],
            "local_info_server_name": self.local_info["server_name"],
            "local_info_gate_id": self.local_info["gate_id"],
            "local_info_gate_name": self.local_info["gate_name"],
            "local_info_city_id": self.local_info["city_id"],
            "local_info_city_name": self.local_info["city_name"],
            "local_info_city_size": self.local_info["city_size"],
            "local_info_city_capacity": self.local_info["city_capacity"],
            "local_info_circle_id": self.local_info["circle_id"],
            "online_support_code": self.online_support_code,
            "capcom_id": self.capcom_id,
            "hunter_name": self.hunter_name,
            "hunter_stats": self.hunter_stats,
            "layer": self.layer,
            "state": self.state,
            "binary_setting": self.binary_setting,
            "hunter_info": self.hunter_info.pack().decode(
                                encoding='ISO-8859-1'
                           )
        }
        return pdict

    @staticmethod
    def deserialize(pdict):
        session = Session(None)
        session.pat_ticket = str(pdict["pat_ticket"])\
            if pdict["pat_ticket"] else pdict["pat_ticket"]
        session.local_info["server_id"] = int(pdict["local_info_server_id"])\
            if pdict["local_info_server_id"] else pdict["local_info_server_id"]
        session.local_info["server_name"] =\
            str(pdict["local_info_server_name"])\
            if pdict["local_info_server_name"]\
            else pdict["local_info_server_name"]
        session.local_info["gate_id"] = int(pdict["local_info_gate_id"])\
            if pdict["local_info_gate_id"] else pdict["local_info_gate_id"]
        session.local_info["gate_name"] = str(pdict["local_info_gate_name"])\
            if pdict["local_info_gate_name"] else pdict["local_info_gate_name"]
        session.local_info["city_id"] = int(pdict["local_info_city_id"])\
            if pdict["local_info_city_id"] else pdict["local_info_city_id"]
        session.local_info["city_name"] = str(pdict["local_info_city_name"])\
            if pdict["local_info_city_name"] else pdict["local_info_city_name"]
        session.local_info["city_size"] = int(pdict["local_info_city_size"])\
            if pdict["local_info_city_size"] else pdict["local_info_city_size"]
        session.local_info["city_capacity"] =\
            int(pdict["local_info_city_capacity"])\
            if pdict["local_info_city_capacity"]\
            else pdict["local_info_city_capacity"]
        session.local_info["circle_id"] = int(pdict["local_info_circle_id"])\
            if pdict["local_info_circle_id"] else pdict["local_info_circle_id"]
        session.online_support_code = str(pdict["online_support_code"])\
            if pdict["online_support_code"] else pdict["online_support_code"]
        session.capcom_id = str(pdict["capcom_id"])
        session.hunter_name = str(pdict["hunter_name"])
        session.hunter_stats = pdict["hunter_stats"]
        session.layer = int(pdict["layer"])
        session.state = int(pdict["state"])
        session.binary_setting = pdict["binary_setting"]
        h_settings = bytearray(pdict["hunter_info"], encoding='ISO-8859-1')
        session.hunter_info = pati.HunterSettings().unpack(h_settings,
                                                           len(h_settings))
        return session

    def get(self, connection_data):
        """Return the session associated with the connection data, if any."""
        has_pat_ticket = hasattr(connection_data, "pat_ticket")
        if has_pat_ticket:
            self.pat_ticket = to_str(
                pati.unpack_binary(connection_data.pat_ticket)
            )
        session = STATE.get_session(self.pat_ticket) or self
        if hasattr(connection_data, "online_support_code"):
            self.online_support_code = to_str(
                pati.unpack_string(connection_data.online_support_code)
            )
        if session != self:
            assert session.connection is None, "Session is already in use"
            session.connection = self.connection
            self.connection = None

        # Preserve session during login process (From OPN to FMP)
        # if no online support code is found
        # Reset upon entering the FMP server (always)
        session.request_reconnection = \
            not ("pat_ticket" in connection_data or
                 "online_support_code" in connection_data)
        return session

    def session_ready(self, connection_data):
        if hasattr(connection_data, "pat_ticket"):
            return STATE.session_ready(to_str(
                pati.unpack_binary(connection_data.pat_ticket)
            ))
        else:
            return STATE.session_ready(self.pat_ticket)

    def set_session_ready(self, connection_data, store_data):
        STATE.set_session_ready(
            to_str(pati.unpack_binary(connection_data.pat_ticket)),
            store_data
        )

    def get_support_code(self):
        """Return the online support code."""
        return DB.get_support_code(self)

    def disconnect(self):
        """Disconnect the current session.

        It doesn't purge the session state nor its PAT ticket.
        """
        self.connection = None
        STATE.disconnect_session(self)

    def delete(self):
        """Delete the current session.

        TODO:
         - Find a good place to purge old tickets.
         - We should probably create a SessionManager thread per server.
        """
        if not self.request_reconnection:
            STATE.delete_session(self)

    def is_jap(self):
        """TODO: Heuristic using the connection data to detect region."""
        pass

    def new_pat_ticket(self):
        # type: () -> str
        STATE.new_pat_ticket(self)
        return self.pat_ticket

    def get_fmp_version(self):
        return STATE.get_servers_version()

    def get_users(self, first_index, count):
        return STATE.get_users(self, first_index, count)

    def use_user(self, index, name):
        STATE.use_user(self, index, name)

    def server_index_exists(self, index):
        try:
            if index in self.loaded_server_ids:
                self.recall_server(index)
                return True
            else:
                return False
        except AssertionError:
            return False

    def preserve_server_ids(self, first_index, count):
        server_ids, servers = STATE.get_servers(include_ids=True)
        if first_index-1 + count > len(server_ids):
            count = len(server_ids) - (first_index - 1)
        assert first_index <= len(server_ids)
        server_ids = server_ids[first_index-1:first_index-1+count]
        self.loaded_server_ids = {}
        for i, server_id in enumerate(server_ids):
            self.loaded_server_ids[first_index+i] = server_id

    def recall_servers(self, first_index, count):
        server_ids, servers = STATE.get_servers(include_ids=True)
        servers = []
        for i in range(first_index, first_index+count):
            servers.append(self.recall_server(i))
        return servers

    def recall_server(self, index):
        return STATE.get_server(self.loaded_server_ids[index])

    def recall_server_id(self, index):
        return self.loaded_server_ids[index]

    def get_servers(self):
        return STATE.get_servers()

    def get_server(self):
        assert self.local_info['server_id'] is not None
        return STATE.get_server(self.local_info['server_id'])

    def get_gate(self):
        assert self.local_info['gate_id'] is not None
        return STATE.get_gate(self.local_info['server_id'],
                              self.local_info['gate_id'])

    def get_city(self):
        assert self.local_info['city_id'] is not None
        return STATE.get_city(self.local_info['server_id'],
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
            if self.local_info['circle_id'] is not None:
                # TODO: Address that circle_id is zero-based
                self.leave_circle()
            self.leave_city()
        if self.layer > 0:
            # Gate path
            self.leave_gate()
            if not self.request_reconnection:
                # Server path (executed at gate and higher)
                self.leave_server()
        elif not self.request_reconnection and self.local_info["server_id"]:
            # Server path (executed if exiting from gate list)
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
            self.create_city(layer_id, settings, optional_fields)
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
        return STATE.layer_detail_search(server_type, fields)

    def join_server(self, server_id):
        return STATE.join_server(self, server_id)

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
            players = STATE.get_all_users(server_id, gate_id, city_id)
        else:
            layer = \
                STATE.get_city(server_id, gate_id, city_id) if city_id else \
                STATE.get_gate(server_id, gate_id) if gate_id else \
                STATE.get_server(server_id)
            players = list(layer.players)
        start = first_index - 1
        return players[start:start+count]

    def find_user_by_capcom_id(self, capcom_id):
        sessions = STATE.find_users(capcom_id=capcom_id)
        if sessions:
            return sessions[0]
        return None

    def find_users(self, capcom_id, hunter_name, first_index, count):
        users = STATE.find_users(capcom_id, hunter_name)
        start = first_index - 1
        return users[start:start+count]

    def get_user_name(self, capcom_id):
        return DB.get_name(capcom_id)

    def leave_server(self):
        STATE.leave_server(self)

    def get_gates(self):
        return STATE.get_gates(self.local_info["server_id"])

    def join_gate(self, gate_id):
        STATE.join_gate(self, self.local_info["server_id"], gate_id)
        self.state = SessionState.GATE

    def leave_gate(self):
        STATE.leave_gate(self)
        self.state = SessionState.LOG_IN

    def get_cities(self):
        return STATE.get_cities(self.local_info["server_id"],
                                self.local_info["gate_id"])

    def is_city_empty(self, city_id):
        return STATE.get_city(self.local_info["server_id"],
                              self.local_info["gate_id"],
                              city_id).get_state() == LayerState.EMPTY

    def reserve_city(self, city_id, reserve):
        return STATE.reserve_city(self.local_info["server_id"],
                                  self.local_info["gate_id"],
                                  city_id, reserve)

    def create_city(self, city_id, settings, optional_fields):
        return STATE.create_city(self,
                                 self.local_info["server_id"],
                                 self.local_info["gate_id"],
                                 city_id, settings, optional_fields)

    def join_city(self, city_id):
        STATE.join_city(self,
                        self.local_info["server_id"],
                        self.local_info["gate_id"],
                        city_id)
        self.state = SessionState.CITY

    def leave_city(self):
        STATE.leave_city(self)
        self.state = SessionState.GATE

    def try_transfer_city_leadership(self):
        if self.local_info['city_id'] is None:
            return None

        city = self.get_city()
        with city.lock():
            if city.leader != self:
                return None

            for _, player in city.players:
                if player == self:
                    continue
                city.leader = player
                return player
        return None

    def try_transfer_circle_leadership(self):
        if self.local_info['circle_id'] is None:
            # TODO: Address that circle_id is zero-based
            return None, None

        circle = self.get_circle()
        with circle.lock(), circle.players.lock():
            if circle.leader != self or circle.get_population() <= 1 \
                    or not circle.departed:
                return None, None
            for i, player in circle.players:
                if player == self:
                    continue
                circle.leader = player
                return i, player
            return None, None

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
        with circle.lock():
            self.local_info['circle_id'] = None
            self.state = SessionState.CITY

            if circle.leader == self:
                circle.reset()
            else:
                circle.players.remove(self)

    def get_layer(self):
        if self.layer == 0:
            return self.get_server()
        elif self.layer == 1:
            return self.get_gate()
        elif self.layer == 2:
            return self.get_city()
        else:
            assert False, "Can't find layer"

    def get_layer_players(self):
        return self.get_layer().players

    def get_layer_path(self):
        return pati.LayerPath(self.local_info['server_id'], self.local_info['gate_id'], 
                              self.local_info['city_id'])

    def get_layer_host_data(self):
        """LayerUserInfo's layer_host."""
        return self.get_layer_path().pack()

    def get_optional_fields(self):
        """LayerUserInfo's optional fields."""
        location = int(self.is_in_quest())  # City - 0, Quest - 1
        hunter_rank = self.hunter_info.rank()
        weapon_type = self.hunter_info.weapon_type()
        return [
                (1, (weapon_type << 24) | location),
                (2, hunter_rank << 16)
        ]

    def add_friend_request(self, capcom_id):
        return DB.add_friend_request(self.capcom_id, capcom_id)

    def accept_friend(self, capcom_id, accepted=True):
        return DB.accept_friend(self.capcom_id, capcom_id, accepted)

    def delete_friend(self, capcom_id):
        return DB.delete_friend(self.capcom_id, capcom_id)

    def get_friends(self, first_index=None, count=None):
        return DB.get_friends(self.capcom_id, first_index, count)
