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

    def get_server_time(self):
        pass

    def get_game_time(self):
        pass

    def get_server_list(self):
        pass

    def get_gates(self, server_id):
        pass


CURRENT_DB = TempDatabase()


def get_instance():
    return CURRENT_DB
