#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Monster Hunter FMP server.

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
from other.utils import server_base, server_main, hexdump
from mh.constants import *
import mh.pat_item as pati


class FmpServer(PatServer):
    """Basic FMP server class."""
    pass


class FmpRequestHandler(PatRequestHandler):
    """Basic FMP server request handler class."""

    def recvAnsConnection(self, packet_id, data, seq):
        """AnsConnection packet."""
        connection_data = pati.ConnectionData.unpack(data)
        self.server.debug("Connection: {!r}".format(connection_data))
        self.sendNtcLogin(3, connection_data, seq)

    def recvReqLayerUserList(self, packet_id, data, seq):
        """ReqLayerUserList packet.

        ID: 64630100
        JP: レイヤ同期ユーザリスト要求
        TR: Layer sync user list request
        """
        count, = struct.unpack_from(">B", data)
        unk = struct.unpack_from(">" + count * "B", data, 1)
        self.sendAnsLayerUserList(unk, seq)

    def sendAnsLayerUserList(self, unk, seq):
        """AnsLayerUserList packet.

        ID: 64630200
        JP: レイヤ同期ユーザリスト返答
        TR: Layer sync user list response
        """

        players = self.session.get_layer_players()
        count = len(players)
        data = struct.pack(">I", count)

        for player in players:
            user = pati.LayerUserInfo()
            user.capcom_id = pati.String(player.capcom_id)
            user.hunter_name = pati.String(player.hunter_name)
            # TODO: Other fields?
            data += user.pack()
        self.send_packet(PatID4.AnsLayerUserList, data, seq)

    def recvReqLayerHost(self, packet_id, data, seq):
        """ReqLayerHost packet.

        ID: 64410100
        JP: レイヤのホスト者要求
        TR: Layer host request
        """

        self.sendAnsLayerHost(data, seq)

    def sendAnsLayerHost(self, unk_data, seq):
        """AnsLayerHost packet.

        ID: 64410200
        JP: レイヤのホスト者返答
        TR: Layer host response
        """

        city = self.session.get_city()
        leader = city.leader
        assert leader != self.session

        leader_handler = self.server.get_pat_handler(leader)

        self.server.debug("ReqLayerHost: Req ({}, {})  Host ({}, {})".
                          format(self.session.capcom_id, self.session.hunter_name, leader.capcom_id,
                                 leader.hunter_name))

        data = unk_data
        data += pati.lp2_string(leader.capcom_id)
        data += pati.lp2_string(leader.hunter_name)
        self.send_packet(PatID4.AnsLayerHost, data, seq)

        # Notify the leader, being the host
        # leader_handler.send_packet(PatID4.NtcLayerHost, data, seq)

        # Notify the city leader of the joining player
        user = pati.LayerUserInfo()
        user.capcom_id = pati.String(self.session.capcom_id)
        user.hunter_name = pati.String(self.session.hunter_name)

        data = pati.lp2_string(self.session.capcom_id)
        data += user.pack()

        leader_handler.send_packet(PatID4.NtcLayerIn, data, seq)

    def recvNtcLayerBinary(self, packet_id, data, seq):
        """NtcLayerBinary packet.

        ID: 64701000
        JP: レイヤユーザ用バイナリ通知
        TR: Binary notifications for layer users
        """

        sender_blank = pati.LayerUserInfo.unpack(data)
        unk_data = data[len(sender_blank.pack()):]
        self.sendNtcLayerBinary(unk_data, seq)

    def sendNtcLayerBinary(self, unk_data, seq):
        """NtcLayerBinary packet.

        ID: 64701000
        JP: レイヤユーザ用バイナリ送信
        TR: Binary transmission for layer users
        """

        sender = pati.LayerBinaryInfo()
        sender.unk_long_0x01 = pati.Long(0x12345678)
        sender.capcom_id = pati.String(self.session.capcom_id)
        sender.hunter_name = pati.String(self.session.hunter_name)

        self.server.debug("NtcLayerBinary: From ({}, {})".format(self.session.capcom_id, self.session.hunter_name))

        data = pati.lp2_string(self.session.capcom_id)
        data += sender.pack()
        data += unk_data

        self.server.layer_broadcast(self.session, PatID4.NtcLayerBinary, data, seq)

    def recvNtcLayerBinary2(self, packet_id, data, seq):
        """NtcLayerBinary packet.

        ID: 64751000
        JP: レイヤユーザ用バイナリ通知 (相手指定)
        TR: Binary notification for layer users (specify the other party)
        """

        partner = pati.unpack_lp2_string(data)
        partner_size = len(partner) + 2
        binary_info = pati.LayerBinaryInfo.unpack(data, partner_size)
        unk_data = data[partner_size + len(binary_info.pack()):]

        self.server.debug("NtcLayerBinary2: From ({}, {})\n{}".format(self.session.capcom_id, self.session.hunter_name,
                                                                      hexdump(unk_data)))

        self.sendNtcLayerBinary2(partner, unk_data, seq)

    def sendNtcLayerBinary2(self, partner, unk_data, seq):
        """NtcLayerBinary packet.

        ID: 64751000
        JP: レイヤユーザ用バイナリ通知 (相手指定)
        TR: Binary transmission for layer users (specify the other party)
        """

        city = self.session.get_city()
        partner_session = next(p for p in city.players if p.capcom_id == partner)
        if partner_session is None:
            return

        data = pati.lp2_string(self.session.capcom_id)

        self_data = pati.LayerBinaryInfo()
        self_data.capcom_id = pati.String(self.session.capcom_id)
        self_data.hunter_name = pati.String(self.session.hunter_name)

        data += self_data.pack()
        data += unk_data

        partner_pat_handler = self.server.get_pat_handler(partner_session)
        if partner_pat_handler is None:
            return

        partner_pat_handler.send_packet(PatID4.NtcLayerBinary2, data, seq)

    def recvReqLayerUp(self, packet_id, data, seq):
        """ReqLayerUp packet.

        ID: 64150100
        JP: レイヤアップ要求
        TR: Layer up request

        Sent by the game when leaving the gate via the entrance:
         - Relocate > Select Server
        """

        if self.session.layer == 2:
            city = self.session.get_city()
            if city.leader == self.session:
                if len(city.players) > 1:
                    # TODO: Transfer the leadership to another player
                    pass
                city.leader = None

            ntc_data = pati.lp2_string(self.session.capcom_id)
            self.server.layer_broadcast(self.session, PatID4.NtcLayerOut, ntc_data, seq)
        self.sendAnsLayerUp(data, seq)

    def recvReqUserSearchInfoMine(self, packet_id, data, seq):
        """ReqUserSearchInfoMine packet.

        ID: 66370100
        JP: ユーザ検索データ要求(自分)
        TR: User search data request (mine)
        """

        search_info = pati.UserSearchInfo.unpack(data)
        self.server.debug("SearchInfo: {!r}".format(search_info))
        self.sendAnsUserSearchInfoMine(search_info, seq)

    def sendAnsUserSearchInfoMine(self, search_info, seq):
        """AnsUserSearchInfoMine packet.

        ID: 66370200
        JP: ユーザ検索データ返答(自分)
        TR: User search data response (mine)

        TODO: Figure out what to do with it.
        Maybe prevent the same profile to be connected twice simultaneously.
        """

        info_mine_0x0f = int(hash(self.session.capcom_id)) & 0xffffffff
        info_mine_0x10 = int(hash(self.session.capcom_id[::-1])) & 0xffffffff

        self.server.debug("SearchInfoMine: {:08X} {:08X}".format(info_mine_0x0f, info_mine_0x10))

        search_info = pati.UserSearchInfo()

        # This fields are used to identify a user. Specifically when a client is deserializing data from the packets
        # `NtcLayerBinary` and `NtcLayerBinary2`
        # TODO: Proper field value and name
        search_info.info_mine_0x0f = pati.Long(info_mine_0x0f)
        search_info.info_mine_0x10 = pati.Long(info_mine_0x10)
        data = search_info.pack()

        self.send_packet(PatID4.AnsUserSearchInfoMine, data, seq)


BASE = server_base("FMP", FmpServer, FmpRequestHandler)

if __name__ == "__main__":
    server_main(*BASE)
