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

RESERVE_DC_TIMEOUT = 40.0


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
                "******", "******", "******",
                "******", "******", "******"
            ]
        return support_code

    def get_capcom_ids(self, online_support_code):
        """Get the Capcom IDs associated with an online support code."""
        return self.consoles[online_support_code]

    def assign_capcom_id(self, online_support_code, index, capcom_id):
        """Assign a Capcom ID to an online support code."""
        self.consoles[online_support_code][index] = capcom_id


CURRENT_DB = TempDatabase()


def get_instance():
    return CURRENT_DB
