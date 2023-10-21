#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2021-2023 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Monster Hunter OPN server."""

from mh.pat import PatServer, PatRequestHandler

from other.utils import server_base, server_main, wii_ssl_wrap_socket


class OpnServer(PatServer):
    """Basic OPN server class."""
    def __init__(self, address, handler_class,
                max_thread_count=0, logger=None, debug_mode=False,
                ssl_cert=None, ssl_key=None):
        super(OpnServer, self).__init__(address, handler_class, 
                max_thread_count=max_thread_count,
                logger=logger, debug_mode=debug_mode)
        self.ssl_cert = ssl_cert
        self.ssl_key = ssl_key


class OpnRequestHandler(PatRequestHandler):
    """Basic OPN server request handler class."""
    def __init__(self, socket, client_address, server):
        if server.ssl_cert is not None and server.ssl_key is not None:
            socket = wii_ssl_wrap_socket(socket, server.ssl_cert, server.ssl_key)
        super(OpnRequestHandler, self).__init__(socket, client_address, server)


BASE = server_base("OPN", OpnServer, OpnRequestHandler)


if __name__ == "__main__":
    server_main(*BASE)
