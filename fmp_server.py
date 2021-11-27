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
from other.utils import server_base, server_main
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

    def sendAnsLayerUserList(self, unk, seq):
        """AnsLayerUserList packet.
        ID: 64630200
        JP: レイヤ同期ユーザリスト返答
        TR: Layer sync user list response
        """

        if self.session.layer == 0:
            server = self.session.get_server()
            players = server.players
        elif self.session.layer == 1:
            gate = self.session.get_gate()
            players = gate.players
        elif self.session.layer == 2:
            city = self.session.get_city()
            players = city.players
        else:
            assert False, "Can't find layer"

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
        leader_handler.send_packet(PatID4.NtcLayerHost, data, seq)

        # Notify the city leader of the joining player
        user = pati.LayerUserInfo()
        user.capcom_id = pati.String(self.session.capcom_id)
        user.hunter_name = pati.String(self.session.hunter_name)

        data = pati.lp2_string(self.session.capcom_id)
        data += user.pack()

        leader_handler.send_packet(PatID4.NtcLayerIn, data, seq)

    def recvNtcLayerBinary(self, packet_id, data, seq):
        sender_blank = pati.LayerUserInfo.unpack(data)
        unk_data = data[len(sender_blank.pack()):]
        self.sendNtcLayerBinary(unk_data, seq)

    def sendNtcLayerBinary(self, unk_data, seq):
        sender = pati.LayerBinaryInfo()
        sender.unk_long_0x01 = pati.Long(0x12345678)
        sender.capcom_id = pati.String(self.session.capcom_id)
        sender.hunter_name = pati.String(self.session.hunter_name)

        self.server.debug("NtcLayerBinary: From ({}, {})".format(self.session.capcom_id, self.session.hunter_name))

        data = pati.lp2_string(self.session.capcom_id)
        data += sender.pack()
        data += unk_data

        city = self.session.get_city()
        for player_session in city.players:
            if player_session == self.session:
                continue

            player_pat_handler = self.server.get_pat_handler(player_session)
            if player_pat_handler is None:
                continue

            player_pat_handler.send_packet(PatID4.NtcLayerBinary, data, seq)

    def recvNtcLayerBinary2(self, packet_id, data, seq):

        self.server.debug("NtcLayerBinary2: From ({}, {})".format(self.session.capcom_id, self.session.hunter_name))

        partner = pati.unpack_lp2_string(data)
        partner_size = len(partner) + 2
        binary_info = pati.LayerBinaryInfo.unpack(data, partner_size)
        unk_data = data[partner_size + len(binary_info.pack()):]
        self.sendNtcLayerBinary2(partner, unk_data, seq)

    def sendNtcLayerBinary2(self, partner, unk_data, seq):
        city = self.session.get_city()
        partner_session = next(p for p in city.players if p.capcom_id == partner)
        if partner_session is None:
            return

        data = pati.lp2_string(self.session.capcom_id)

        self_data = pati.LayerUserInfo()
        self_data.capcom_id = pati.String(self.session.capcom_id)
        self_data.hunter_name = pati.String(self.session.hunter_name)

        data += self_data.pack()
        data += unk_data

        partner_pat_handler = self.server.get_pat_handler(partner_session)
        if partner_pat_handler is None:
            return

        partner_pat_handler.send_packet(PatID4.NtcLayerBinary2, data, seq)

    def recvReqLayerUp(self, packet_id, data, seq):
        if self.session.layer == 2:
            city = self.session.get_city()
            if city.leader == self.session:
                if len(city.players) > 1:
                    # TODO: Transfer the leadership to another player
                    pass
                city.leader = None

            ntc_layer_out_data = pati.lp2_string(self.session.capcom_id)
            for player_in_city in city.players:
                if player_in_city == self.session:
                    continue

                player_in_city_handler = self.server.get_pat_handler(player_in_city)
                if player_in_city_handler is None:
                    continue

                player_in_city_handler.send_packet(PatID4.NtcLayerOut, ntc_layer_out_data, 0)
        self.sendAnsLayerUp(data, seq)

BASE = server_base("FMP", FmpServer, FmpRequestHandler)

if __name__ == "__main__":
    server_main(*BASE)
