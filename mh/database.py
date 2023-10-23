#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2021-2023 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Monster Hunter database module."""

import random
import sqlite3
import time
from other import utils
from threading import RLock, local as thread_local


CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

MEDIA_VERSIONS = {
    "0903131810": "ROMJ08",
    "0906222136": "RMHJ08",
    "1001301045": "RMHE08",
    "1002121503": "RMHP08",
}

BLANK_CAPCOM_ID = "******"

def new_random_str(length=6):
    return "".join(random.choice(CHARSET) for _ in range(length))


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
        self.capcom_ids = {
            # Capcom ID => Hunter name
        }
        self.friend_requests = {
            # Capcom ID => List of friend requests from Capcom IDs
        }
        self.friend_lists = {
            # Capcom ID => List of Capcom IDs
            # TODO: May need stable index, see Players class
        }

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

    def get_capcom_ids(self, online_support_code):
        """Get the Capcom IDs associated with an online support code."""
        return self.consoles[online_support_code]

    def assign_capcom_id(self, online_support_code, index, capcom_id):
        """Assign a Capcom ID to an online support code."""
        self.consoles[online_support_code][index] = capcom_id

    def assign_name(self, capcom_id, name):
        self.capcom_ids[capcom_id] = name

    def get_name(self, capcom_id):
        return self.capcom_ids.get(capcom_id, "")

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
            (k, self.capcom_ids[k])
            for k in self.friend_lists[capcom_id]
            if k in self.capcom_ids  # Skip unknown Capcom IDs
        ][begin:end]


class SafeSqliteConnection(object):
    """Safer SQLite connection wrapper."""

    def __init__(self, *args, **kwargs):
        self.__connection = sqlite3.connect(*args, **kwargs)
        self.__connection.row_factory = sqlite3.Row
        # Avoid "unicode argument without an encoding" error
        # Fix python2/3 text_factory = str vs bytes
        # NB: data types aren't enforced
        self.__connection.text_factory = utils.to_str

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
                # Enforcing BLOB type since sometimes it's retrieved as TEXT
                name = utils.to_bytes(name)
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
                    info = self.capcom_ids.get(capcom_id, {"name": b""})
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

    def assign_capcom_id(self, online_support_code, index, capcom_id):
        """Assign a Capcom ID to an online support code."""
        self.consoles[online_support_code][index] = capcom_id
        with self.connection as cursor:
            cursor.execute(
                "INSERT OR REPLACE INTO consoles VALUES (?,?,?,?)",
                (online_support_code, index, capcom_id, "????")
            )

    def get_capcom_ids(self, online_support_code):
        """Get list of associated Capcom IDs from an online support code."""
        with self.connection as cursor:
            rows = cursor.execute("SELECT slot_index, capcom_id FROM consoles WHERE support_code = '{}'".format(online_support_code))
            ids = []
            for index, id in rows:
                while len(ids) < index:
                    ids.append(BLANK_CAPCOM_ID)
                ids.append(id)
            while len(ids) < 6:
                ids.append(BLANK_CAPCOM_ID)
            return ids

    def get_name(self, capcom_id):
        """Get the hunter name associated with a valid Capcom ID."""
        with self.connection as cursor:
            rows = cursor.execute("SELECT name FROM consoles WHERE capcom_id = '{}'".format(capcom_id))
            names = [name for name, in rows]
            if len(names):
                return names[0]
            return ""

    def use_user(self, session, index, name):
        """Insert the current hunter's info into a selected Capcom ID slot."""
        with self.connection as cursor:
            cursor.execute(
                "INSERT OR REPLACE INTO consoles VALUES (?,?,?,?)",
                (session.online_support_code, index,
                 session.capcom_id, session.hunter_name)
            )

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

    def get_friends(self, capcom_id, first_index=None, count=None):
        begin = 0 if first_index is None else (first_index - 1)
        end = count if count is None else (begin + count)
        with self.connection as cursor:
            rows = cursor.execute("SELECT friend_id, name FROM friend_lists INNER JOIN consoles ON friend_lists.friend_id = consoles.capcom_id WHERE friend_lists.capcom_id = '{}'".format(capcom_id))
            friends = []
            for friend_id, name in rows:
                friends.append((friend_id, name))
            return friends[begin:end]


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
