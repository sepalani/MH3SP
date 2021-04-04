#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Monster Hunter PAT module.

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

import select

from other.utils import Logger

try:
    # Python 3
    import socketserver as SocketServer
except ImportError:
    # Python 2
    import SocketServer


class PatServer(SocketServer.TCPServer, Logger):
    """Generic PAT server class."""

    def __init__(self, address, handler_class, logger=None):
        SocketServer.TCPServer.__init__(self, address, handler_class)
        Logger.__init__(self)
        if logger:
            self.set_logger(logger)
        self.info("Running on {} port {}".format(*address))
        self.debug_con = []

    def add_to_debug(self, con):
        """Add connection to the debug connection list."""
        self.debug_con.append(con)

    def del_from_debug(self, con):
        """Delete connection from the debug connection list."""
        self.debug_con.remove(con)

    def get_debug(self):
        """Return the debug connection list."""
        return self.debug_con


class PatRequestHandler(SocketServer.StreamRequestHandler):
    """Generic PAT request handler class."""

    def handle(self):
        self.server.info("Handle client")
        self.server.add_to_debug(self)

        while True:
            r, w, e = select.select([self.rfile], [self.wfile], [], 0.2123)
            if r:
                self.server.debug("<<< Reading header...")
                data = self.rfile.read(8)
                if not len(data):
                    break
                self.server.debug("<<< Reading data...")
            if w:
                pass
            if e:
                break

        self.server.del_from_debug(self)
        self.server.info("Client finished!")
