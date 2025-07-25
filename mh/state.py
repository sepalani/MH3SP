#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2023-2025 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""FMP server state module.

Each FMP server needs to know the in-game resources it manages:
 - Servers
 - Gates
 - Cities
 - Sessions (i.e. active server connections)

TODO/FIXME:
Our current design isn't very scalable.
"""


from mh.database import get_instance as get_db
from mh.state_models import Server, ServerType

try:
    from typing import TypedDict, TYPE_CHECKING
    if TYPE_CHECKING:
        from mh.session import Session
        from mh.state_models import Gate, City  # noqa: F401

        CapcomIDsInfo = TypedDict("CapcomIDsInfo", {
            "name": bytes,
            "session": None | Session
        })
except (ImportError, TypeError):
    pass


def new_servers():
    # type: () -> list[Server]
    # TODO: This logic was removed upstream to use harcoded values...
    servers = []  # type: list[Server]
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
    """FMP server state class.

    Holds the required information not to bother too frequently:
     - the database server
     - the central server

    Ideally, this should allow the server to be resilient and operate even
    with limited connectivity to the database and central server.

    TODO: (backport)
     - Backport cache/server_id logic
     - Like the following methods if needed:
     setup_server
     register_pat_ticket
     get_session
     disconnect_session
     delete_session (+ cache logic)
     fetch_id
     get_servers_version
     update_players
     update_capcom_id
     session_ready
     set_session_ready
     close_cache

    FIXME: (backport)
     - These methods should belong to db (imho)
    new_pat_ticket -> db.generate_pat_ticket + fill self.session
    use_capcom_id
    use_user
    get_users (i.e. LMP server)
    """
    def __init__(self):
        self.servers = new_servers()
        # TODO: Backport Sessions/Capcom ID handling (currently unused)
        self.sessions = {
            # PAT Ticket => Owner's session
        }  # type: dict[str, Session]
        self.capcom_ids = {
            # Capcom ID => Owner's name and session
            # NB: Not to be mistaken with database.capcom_ids!
        }  # type: dict[str, CapcomIDsInfo]

    def join_server(self, session, index):
        # type: (Session, int) -> Server
        if session.local_info["server_id"] is not None:
            self.leave_server(session, session.local_info["server_id"])
        # TODO: Backport cache/joining another external server
        # It might imply moving from (array) index to (dict) server_id
        server = self.get_server(index)
        server.players.add(session)
        session.local_info["server_id"] = index
        session.local_info["server_name"] = server.name
        return server

    def leave_server(self, session, index):
        # type: (Session, int) -> None
        self.get_server(index).players.remove(session)
        session.local_info["server_id"] = None
        session.local_info["server_name"] = None

    def get_server_time(self):
        # TODO: Use it at some point or remove it
        pass

    def get_game_time(self):
        # TODO: Use it at some point or remove it
        pass

    def get_servers(self):
        # type: () -> list[Server]
        # TODO: Backport cache code
        return self.servers

    def get_server(self, index):
        # type: (int) -> Server
        # TODO: Backport cache code
        assert 0 < index <= len(self.servers), "Invalid server index"
        return self.servers[index - 1]

    def get_gates(self, server_id):
        # type: (int) -> list[Gate]
        return self.get_server(server_id).gates

    def get_gate(self, server_id, index):
        # type: (int, int) -> Gate
        gates = self.get_gates(server_id)
        assert 0 < index <= len(gates), "Invalid gate index"
        return gates[index - 1]

    def join_gate(self, session, server_id, index):
        # type: (Session, int, int) -> Gate
        gate = self.get_gate(server_id, index)
        gate.parent.players.remove(session)
        gate.players.add(session)
        session.local_info["gate_id"] = index
        session.local_info["gate_name"] = gate.name
        return gate

    def leave_gate(self, session):
        # type: (Session) -> None
        gate = self.get_gate(session.local_info["server_id"],
                             session.local_info["gate_id"])
        gate.parent.players.add(session)
        gate.players.remove(session)
        session.local_info["gate_id"] = None
        session.local_info["gate_name"] = None

    def get_cities(self, server_id, gate_id):
        # type: (int, int) -> list[City]
        return self.get_gate(server_id, gate_id).cities

    def get_city(self, server_id, gate_id, index):
        # type: (int, int, int) -> City
        cities = self.get_cities(server_id, gate_id)
        assert 0 < index <= len(cities), "Invalid city index"
        return cities[index - 1]

    def reserve_city(self, server_id, gate_id, index, reserve):
        # type: (int, int, int, bool) -> bool
        city = self.get_city(server_id, gate_id, index)
        with city.lock():
            if reserve and city.is_reserved():
                return False
            city.reserve(reserve)
        return True

    def get_all_users(self, server_id, gate_id, city_id):
        # type: (int, int, None | int) -> list[tuple[int, Session]]
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

    def find_users(self, capcom_id="", hunter_name=b""):
        # type: (str, bytes) -> list[Session]
        assert capcom_id or hunter_name, "Search can't be empty"
        users = []  # type: list[Session]
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
        # TODO: Backport cache/central code
        # FIXME: We need to rely on DB meanwhile...
        assert len(users) == 0, "State doesn't save IDs/Session yet"
        users.extend(get_db().find_users(
            capcom_id=capcom_id,
            hunter_name=hunter_name
        ))
        return users

    def create_city(self, session, server_id, gate_id, index,
                    settings, optional_fields):
        city = self.get_city(server_id, gate_id, index)
        with city.lock():
            city.optional_fields = optional_fields
            city.leader = session
        return city

    def join_city(self, session, server_id, gate_id, index):
        # type: (Session, int, int, int) -> City
        city = self.get_city(server_id, gate_id, index)
        with city.lock():
            city.parent.players.remove(session)
            city.players.add(session)
            session.local_info["city_name"] = city.name
        session.local_info["city_id"] = index
        return city

    def leave_city(self, session):
        # type: (Session) -> None
        city = self.get_city(session.local_info["server_id"],
                             session.local_info["gate_id"],
                             session.local_info["city_id"])
        with city.lock():
            city.parent.players.add(session)
            city.players.remove(session)
            if not city.get_population():
                city.clear_circles()
        session.local_info["city_id"] = None
        session.local_info["city_name"] = None

    def layer_detail_search(self, server_type, fields):
        # TODO: Better document and test this
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
