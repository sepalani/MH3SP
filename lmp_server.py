#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2021 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Monster Hunter LMP server."""

from mh.pat import PatServer, PatRequestHandler
from other.utils import server_base, server_main

import mh.pat_item as pati


class LmpServer(PatServer):
    """Basic LMP server class."""
    pass


class LmpRequestHandler(PatRequestHandler):
    """Basic LMP server request handler class."""

    def recvAnsConnection(self, packet_id, data, seq):
        """AnsConnection packet."""
        connection_data = pati.ConnectionData.unpack(data)
        self.server.debug("Connection: {!r}".format(connection_data))
        if hasattr(connection_data, "pat_ticket"):
            self.sendNtcLogin(2, connection_data, seq)
        else:
            self.sendNtcLogin(1, connection_data, seq)


BASE = server_base("LMP", LmpServer, LmpRequestHandler)


if __name__ == "__main__":
    server_main(*BASE)
