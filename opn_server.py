#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2021-2023 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Monster Hunter OPN server."""

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
