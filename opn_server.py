#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2021-2023 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Monster Hunter OPN server."""

import mh.pat_item as pati
from mh.pat import PatServer, PatRequestHandler

from other.utils import server_base, server_main, to_str


class OpnServer(PatServer):
    """Basic OPN server class."""
    pass


class OpnRequestHandler(PatRequestHandler):
    """Basic OPN server request handler class."""
    # TODO: Backport wii_ssl_wrap_socket change if needed

    def sendReqConnection(self, unused=0, seq=0):
        """Override default implementation to add security checks."""
        self.sendReqMemoryCheck(0x80000000, 6)  # Request the game id

    def recvAnsMemoryCheck(self, packet_id, data, seq):
        """AnsMemoryCheck packet.

        ID: 60810200
        JP: メモリ内容送信
        TR: Memory content transmission
        """
        # unk = pati.MemoryData.unpack(data)
        # with pati.Unpacker(data, offset=len(unk.pack())) as unpacker:
        with pati.Unpacker(data) as unpacker:
            unk = unpacker.MemoryData()
            address, = unpacker.struct(">I")
            data = unpacker.lp2_string()

            if address == 0x80000000:
                self.game_id = to_str(data) # type: ignore
                if self.game_id == 'RMHE08':
                    self.sendReqMemoryCheck(0x806308e8, 56)
                elif self.game_id == 'RMHP08':
                    self.sendReqMemoryCheck(0x806311a8, 56)
                else:
                    PatRequestHandler.sendReqConnection(self)
            elif address in [0x806308e8, 0x806311a8]:
                # TODO: Backport the patch checking logic
                PatRequestHandler.sendReqConnection(self)


BASE = server_base("OPN", OpnServer, OpnRequestHandler)


if __name__ == "__main__":
    server_main(*BASE)
