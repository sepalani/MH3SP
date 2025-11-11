#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2025 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""FMP server state models module.

This module contains ORM-like models to be (de)serialized.
"""

import time

from threading import RLock

try:
    from typing import Any, Literal, TYPE_CHECKING  # noqa: F401

    ServerTypeLiteral = Literal[1, 2, 3, 4]
    LayerStateLiteral = Literal[0, 1, 2]

    if TYPE_CHECKING:
        # FIXME: Session.deserialize introduces cyclic import
        from mh.session import Session
except (ImportError, TypeError):
    pass


RESERVE_DC_TIMEOUT = 40.0


class ServerType:
    OPEN = 1
    ROOKIE = 2
    EXPERT = 3
    RECRUITING = 4


class LayerState:
    JOINABLE = 0
    EMPTY = 1
    FULL = 2


class Lockable(object):
    def __init__(self):
        self._lock = RLock()

    def lock(self):
        return self

    def __enter__(self):
        # Returns True if lock was acquired, False otherwise
        return self._lock.acquire()

    def __exit__(self, *args):
        # type: (Any) -> None
        self._lock.release()


class Players(Lockable):
    """Helper class to help retain player IDs."""
    def __init__(self, capacity):
        # type: (int) -> None
        assert capacity > 0, "Collection capacity can't be zero"

        self.slots = [
            None for _ in range(capacity)
        ]  # type: list[None | Session]
        self.used = 0
        super(Players, self).__init__()

    def get_used_count(self):
        # type: () -> int
        return self.used

    def get_capacity(self):
        # type: () -> int
        return len(self.slots)

    def add(self, item):
        # type: (Session) -> int
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
        # type: (Session | int) -> bool
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
        # type: (Session) -> int
        assert item is not None, "Item != None"

        for i, v in enumerate(self.slots):
            if v == item:
                return i

        return -1

    def clear(self):
        # type: () -> None
        with self.lock():
            for i in range(self.get_capacity()):
                self.slots[i] = None

    def find_first(self, **kwargs):
        # type: (Any) -> None | Session
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
        # type: (str) -> None | Session
        return self.find_first(capcom_id=capcom_id)

    def __len__(self):
        return self.used

    def __iter__(self):
        if self.used < 1:
            return

        for i, v in enumerate(self.slots):
            if v is None:
                continue

            yield i, v

    def serialize(self):
        # type: () -> dict[str, Any]
        if not self.used:
            return {"capacity": len(self.slots)}
        return {
            "slots": [
                (p.serialize()
                 if p is not None
                 else None)
                for p in self.slots
            ],
            "used": self.used
        }

    @staticmethod
    def deserialize(obj, parent):
        # type: (dict[str, Any], None) -> Players
        if "used" not in obj.keys():
            return Players(obj["capacity"])

        from mh.session import Session  # avoid cyclic import

        players = Players(len(obj["slots"]))
        players.slots = [
            (Session.deserialize(p)
             if p is not None
             else None)
            for p in obj["slots"]
        ]
        players.used = obj["used"]
        return players


class Circle(Lockable):
    def __init__(self, parent):
        # type: (City) -> None
        self.parent = parent
        self.leader = None  # type: None | Session
        self.players = Players(4)
        self.departed = False
        self.quest_id = 0
        self.embarked = False  # FIXME: Seems never used
        self.password = None
        self.remarks = None

        self.unk_byte_0x0e = 0
        super(Circle, self).__init__()

    def get_population(self):
        # type: () -> int
        return len(self.players)

    def get_capacity(self):
        # type: () -> int
        return self.players.get_capacity()

    def is_full(self):
        # type: () -> bool
        return self.get_population() == self.get_capacity()

    def is_empty(self):
        # type: () -> bool
        return self.leader is None

    def is_joinable(self):
        # type: () -> bool
        return not self.departed and not self.is_full()

    def has_password(self):
        # type: () -> bool
        return self.password is not None

    def reset_players(self, capacity):
        # type: (int) -> None
        with self.lock():
            self.players = Players(capacity)

    def reset(self):
        # type: () -> None
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
        # type: () -> dict[str, Any]
        players = self.players.serialize()
        if "used" not in players.keys():
            return {}
        return {
            "parent": None,
            "leader":
                self.leader.serialize()
                if self.leader is not None
                else None,
            "players": players,
            "departed": self.departed,
            "quest_id": self.quest_id,
            "embarked": self.embarked,
            "password": self.password,
            "remarks": self.remarks,
            "unk_byte_0x0e": self.unk_byte_0x0e
        }

    @staticmethod
    def deserialize(obj, parent):
        # type: (dict[str, Any], City) -> Circle
        circle = Circle(parent)
        if not obj.keys():
            return circle

        from mh.session import Session  # avoid cyclic import

        circle.leader = \
            Session.deserialize(obj["leader"]) \
            if obj["leader"] is not None \
            else None
        # TODO: Players class doesn't have "parent" member variable
        circle.players = Players.deserialize(obj["players"], circle)
        circle.departed = obj["departed"]
        circle.quest_id = obj["quest_id"]
        circle.embarked = obj["embarked"]
        circle.password = obj["password"]
        circle.remarks = obj["remarks"]
        circle.unk_byte_0x0e = obj["unk_byte_0x0e"]
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
            # NB: Might not work on the Japanese version, IIRC the limit is 5
        ]
        super(City, self).__init__()

    def get_population(self):
        # type: () -> int
        return len(self.players)

    def in_quest_players(self):
        # type: () -> int
        return sum(p.is_in_quest() for _, p in self.players)

    def get_capacity(self):
        # type: () -> int
        return self.players.get_capacity()

    def get_state(self):
        # type: () -> LayerStateLiteral
        # FIXME: The following part was removed v
        if self.reserved:
            return LayerState.FULL
        # TODO: ^ Backport it and make sure that wasn't a mistake

        size = self.get_population()
        if size == 0:
            return LayerState.EMPTY
        elif size < self.get_capacity():
            return LayerState.JOINABLE
        else:
            return LayerState.FULL

    def is_empty(self):
        # type: () -> bool
        return self.get_state() == LayerState.EMPTY

    def get_pathname(self):
        # type: () -> str
        pathname = self.name  # type: str
        it = self.parent
        # FIXME: Some tools don't like type-checking this loop at all
        while it is not None:  # type: ignore
            pathname = it.name + "\t" + pathname
            it = it.parent  # type: Gate | Server | None
        return pathname

    def get_first_empty_circle(self):
        # type: () -> tuple[None, None] | tuple[Circle, int]
        with self.lock():
            for index, circle in enumerate(self.circles):
                if circle.is_empty():
                    return circle, index
        return None, None

    def get_circle_for(self, leader_session):
        # type: (Session) -> tuple[None, None] | tuple[Circle, int]
        with self.lock():
            for index, circle in enumerate(self.circles):
                if circle.leader == leader_session:
                    return circle, index
        return None, None

    def clear_circles(self):
        # type: () -> None
        with self.lock():
            for circle in self.circles:
                circle.reset()

    def reserve(self, reserve):
        # type: (bool) -> None
        with self.lock():
            if reserve:
                self.reserved = time.time()
            else:
                self.reserved = None

    def is_reserved(self):
        # type: () -> bool
        reserved_time = self.reserved  # type: None | float
        if reserved_time:
            return time.time()-reserved_time < RESERVE_DC_TIMEOUT
        return False

    def get_all_players(self):
        # type: () -> list[Session]
        with self.players.lock():
            return [p for _, p in self.players]

    def serialize(self):
        # type: () -> dict[str, Any]
        players = self.players.serialize()
        if "used" not in players.keys():
            return {"name": self.name}
        return {
            "name": self.name,
            "parent": None,  # TODO: Why (not) serializing it?
            "state": self.state,
            "players": players,
            "optional_fields": self.optional_fields,
            "leader":
                self.leader.serialize()
                if self.leader is not None
                else None,
            "reserved": self.reserved,
            "circles": [c.serialize() for c in self.circles]
        }

    @staticmethod
    def deserialize(obj, parent):
        # type: (dict[str, Any], Gate) -> City
        if len(obj.keys()) < 2:
            return City(obj["name"], None)
        city = City(
            str(obj["name"]) if obj["name"] is not None else obj["name"],
            parent
        )
        city.state = obj["state"]
        city.players = Players.deserialize(obj["players"], parent)
        city.optional_fields = obj["optional_fields"]
        city.leader = \
            Session.deserialize(obj["leader"]) \
            if obj["leader"] is not None \
            else None
        city.reserved = obj["reserved"]
        city.circles = [Circle.deserialize(c, city) for c in obj["circles"]]
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
        # type: () -> int
        return len(self.players) + sum((
            city.get_population()
            for city in self.cities
        ))

    def get_capacity(self):
        # type: () -> int
        return self.players.get_capacity()

    def get_state(self):
        # type: () -> LayerStateLiteral
        size = self.get_population()
        if size == 0:
            return LayerState.EMPTY
        elif size < self.get_capacity():
            return LayerState.JOINABLE
        else:
            return LayerState.FULL

    def get_all_players(self):
        # type: () -> list[Session]
        # TODO: Backport its use, e.g. in cache
        players = [p for _, p in self.players]
        for city in self.cities:
            players += city.get_all_players()
        return players

    def serialize(self):
        # type: () -> dict[str, Any]
        return {
            "name": self.name,
            "parent": None,
            "state": self.state,
            "cities": [c.serialize() for c in self.cities],
            "players": self.players.serialize(),
            "optional_fields": self.optional_fields
        }

    @staticmethod
    def deserialize(obj, parent):
        # type: (dict[str, Any], Server) -> Gate
        gate = Gate(
            str(obj["name"]) if obj["name"] is not None else obj["name"],
            parent
        )
        gate.state = obj["state"]
        gate.cities = [City.deserialize(c, gate) for c in obj["cities"]]
        gate.players = Players.deserialize(obj["players"], gate)
        gate.optional_fields = obj["optional_fields"]
        return gate


class Server(object):
    LAYER_DEPTH = 1

    def __init__(self, name, server_type, gate_count=40, capacity=2000,
                 addr=None, port=None):
        # type: (str, ServerTypeLiteral, int, int, None | str, None | int) -> None  # noqa: E501
        # TODO: Backport the constructor change if needed
        self.name = name
        self.parent = None
        self.server_type = server_type
        # Public IP address
        self.addr = addr  # type: None | str
        self.port = port  # type: None | int
        self.gates = [
            Gate("City Gate{}".format(i), self)
            for i in range(1, gate_count+1)
        ]
        self.players = Players(capacity)

    def get_population(self):
        # type: () -> int
        return len(self.players) + sum((
            gate.get_population() for gate in self.gates
        ))

    def get_capacity(self):
        # type: () -> int
        return self.players.get_capacity()

    def get_all_players(self):
        # type: () -> list[Session]
        # TODO: Backport its use, e.g. in cache
        players = [p for _, p in self.players]
        for gate in self.gates:
            players = players + gate.get_all_players()
        return players

    def serialize(self):
        # type: () -> dict[str, Any]
        return {
            "name": self.name,
            "parent": self.parent,
            "server_type": self.server_type,
            "addr": self.addr,
            "port": self.port,
            "gates": [g.serialize() for g in self.gates],
            "players": self.players.serialize()
        }

    @staticmethod
    def deserialize(obj):
        # type: (dict[str, Any]) -> Server
        server = Server(
            str(obj["name"]) if obj["name"] is not None
            else obj["name"],
            int(obj["server_type"]) if obj["server_type"]
            else obj["server_type"],
            addr=str(obj["addr"]) if obj["addr"] is not None
            else obj["addr"],
            port=int(obj["port"]) if obj["port"] is not None
            else obj["port"]
        )
        server.parent = obj["parent"]
        server.gates = [Gate.deserialize(g, server) for g in obj["gates"]]
        server.players = Players.deserialize(obj["players"], server)
        return server
