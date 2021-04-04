#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Monster Hunter OPN server.

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

from mh.pat import PatServer, PatRequestHandler
from other.utils import server_base, server_main


class OpnServer(PatServer):
    """Basic OPN server class."""
    pass


class OpnRequestHandler(PatRequestHandler):
    """Basic OPN server request handler class."""
    pass


BASE = server_base("OPN", OpnServer, OpnRequestHandler)


if __name__ == "__main__":
    server_main(*BASE)
