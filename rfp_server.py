#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2021 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Monster Hunter RFP server."""

from mh.pat import PatServer, PatRequestHandler
from other.utils import server_base, server_main


class RfpServer(PatServer):
    """Basic RFP server class."""
    pass


class RfpRequestHandler(PatRequestHandler):
    """Basic RFP server request handler class."""
    pass


BASE = server_base("RFP", RfpServer, RfpRequestHandler)


if __name__ == "__main__":
    server_main(*BASE)
