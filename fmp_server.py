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

    def sendAnsLayerDown(self, layer_id, layer_set, seq):
        """AnsLayerDown packet.

       ID: 64140200
       JP: レイヤダウン返答
       TR: Layer down response
       """

        self.session.layer_down(layer_id)
        if self.session.layer == 1:  # Gate
            user = pati.LayerUserInfo()
            user.capcom_id = pati.String(self.session.capcom_id)
            user.hunter_name = pati.String(self.session.hunter_name)
            user.stats = pati.Binary(self.session.hunter_info.pack())

            data = pati.lp2_string(self.session.capcom_id)
            data += user.pack()

            gate = self.session.get_gate()
            for player in gate.players:
                if self.session == player:
                    continue

                pat_handler = self.server.get_pat_handler(player)
                pat_handler.send_packet(PatID4.NtcLayerIn, data, seq)

        data = struct.pack(">H", layer_id)
        self.send_packet(PatID4.AnsLayerDown, data, seq)

    def recvReqUserBinarySet(self, packet_id, data, seq):
        offset, length = struct.unpack_from(">IH", data)
        binary = pati.unpack_lp2_string(data, 4)
        self.session.hunter_info.unpack(data[6:], length, offset)

        # unk1 ??
        self.sendAnsUserBinarySet(offset, binary, seq)

    def recvReqUserBinaryNotice(self, packet_id, data, seq):
        unk1, = struct.unpack_from(">B", data)
        capcom_id = pati.unpack_lp2_string(data, 1)
        offset, length = struct.unpack_from(">II", data, 3 + len(capcom_id))

        self.sendAnsUserBinaryNotice(unk1, capcom_id, offset, length, seq)

    def sendAnsUserBinaryNotice(self, unk1, capcom_id, offset, length, seq):
        data = struct.pack(">B", unk1)
        data += pati.lp2_string(self.session.capcom_id)
        data += struct.pack(">I", 0)

        data += pati.lp2_string(self.session.hunter_info.pack())

        players = self.session.get_layer_players()
        for player in players:
            if player == self.session:
                continue

            pat_handler = self.server.get_pat_handler(player)
            pat_handler.send_packet(PatID4.NtcUserBinaryNotice, data, seq)

        self.send_packet(PatID4.AnsUserBinaryNotice, b"", seq)

    def sendAnsLayerUserList(self, unk, seq):
        """AnsLayerUserList packet.
        ID: 64630200
        JP: レイヤ同期ユーザリスト返答
        TR: Layer sync user list response
        """

        players = self.session.get_layer_players()
        data = struct.pack(">I", len(players))

        for player in players:
            user = pati.LayerUserInfo()
            user.capcom_id = pati.String(player.capcom_id)
            user.hunter_name = pati.String(player.hunter_name)
            user.stats = pati.Binary(player.hunter_info.pack())
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

        self.server.debug("ReqLayerHost: Req ({}, {})  Host ({}, {})".format(
            self.session.capcom_id, self.session.hunter_name,
            leader.capcom_id, leader.hunter_name))

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
        user.stats = pati.Binary(self.session.hunter_info.pack())

        data = pati.lp2_string(self.session.capcom_id)
        data += user.pack()

        leader_handler.send_packet(PatID4.NtcLayerIn, data, seq)

    def recvNtcLayerUserPosition(self, packet_id, data, seq):
        self.sendNtcLayerUserPosition(data, seq)

    def sendNtcLayerUserPosition(self, fo, seq):

        assert self.session.layer == 2  # Make sure to be in a city
        city = self.session.get_city()

        data = pati.lp2_string(self.session.capcom_id)
        data += fo

        for player_in_city in city.players:
            if player_in_city == self.session:
                continue

            player_pat_handler = self.server.get_pat_handler(player_in_city)
            player_pat_handler.send_packet(PatID4.NtcLayerUserPosition,
                                           data, seq)

    def recvNtcLayerBinary(self, packet_id, data, seq):
        sender_blank = pati.LayerUserInfo.unpack(data)
        unk_data = data[len(sender_blank.pack()):]
        self.sendNtcLayerBinary(unk_data, seq)

    def sendNtcLayerBinary(self, unk_data, seq):
        sender = pati.LayerBinaryInfo()
        sender.unk_long_0x01 = pati.Long(0x12345678)
        sender.capcom_id = pati.String(self.session.capcom_id)
        sender.hunter_name = pati.String(self.session.hunter_name)

        self.server.debug("NtcLayerBinary: From ({}, {})".format(
            self.session.capcom_id, self.session.hunter_name))

        data = pati.lp2_string(self.session.capcom_id)
        data += sender.pack()
        data += unk_data

        players = self.session.get_layer_players()
        for player_session in players:
            if player_session == self.session:
                continue

            player_pat_handler = self.server.get_pat_handler(player_session)
            if player_pat_handler is None:
                continue

            player_pat_handler.send_packet(PatID4.NtcLayerBinary, data, seq)

    def recvNtcLayerBinary2(self, packet_id, data, seq):

        partner = pati.unpack_lp2_string(data)
        partner_size = len(partner) + 2
        binary_info = pati.LayerBinaryInfo.unpack(data, partner_size)
        unk_data = data[partner_size + len(binary_info.pack()):]

        self.server.debug("NtcLayerBinary2: From ({}, {})\n{}".format(
            self.session.capcom_id, self.session.hunter_name,
            hexdump(unk_data)))

        self.sendNtcLayerBinary2(partner, unk_data, seq)

    def sendNtcLayerBinary2(self, partner, unk_data, seq):
        city = self.session.get_city()
        partner_session = next(p for p in city.players
                               if p.capcom_id == partner)
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

                player_in_city_handler = self.server\
                    .get_pat_handler(player_in_city)
                if player_in_city_handler is None:
                    continue

                player_in_city_handler.send_packet(PatID4.NtcLayerOut,
                                                   ntc_layer_out_data, 0)
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

        self.server.debug("SearchInfoMine: {:08X} {:08X}"
                          .format(info_mine_0x0f, info_mine_0x10))

        search_info = pati.UserSearchInfo()
        search_info.info_mine_0x0f =\
            pati.Long(info_mine_0x0f)  # TODO: Proper field value
        search_info.info_mine_0x10 =\
            pati.Long(info_mine_0x10)  # TODO: Proper field value
        data = search_info.pack()

        self.send_packet(PatID4.AnsUserSearchInfoMine, data, seq)

    def recvReqCircleListLayer(self, packet_id, data, seq):
        """ReqCircleListLayer packet.

        ID: 65270100
        JP: サークル同期リスト要求 (レイヤ)
        TR: Circle sync list request (layer)
        """
        self.sendAnsCircleListLayer(data, seq)

    def sendAnsCircleListLayer(self, data, seq):
        """AnsCircleListLayer packet.

        ID: 65270200
        JP: サークル同期リスト返答 (レイヤ)
        TR: Circle sync list response (layer)
        """
        unk = 0
        circles = []

        city = self.session.get_city()
        for i in range(0, len(city.circles)):
            circle = city.circles[i]
            if circle.is_empty():
                continue

            info = pati.CircleInfo()
            info.index = pati.Long(i + 1)
            info.leader_capcom_id = pati.String(circle.leader.capcom_id)
            info.has_password = pati.Byte(1 if circle.has_password() else 0)
            info.team_size = pati.Long(circle.capacity)

            if circle.remarks is not None:
                info.remarks = pati.String(circle.remarks)

            extra_info = []
            extra_info.append((1, circle.get_capacity()))
            extra_info.append((2, circle.questId))
            # TODO: Other extra values

            circles.append([info, extra_info])

        count = len(circles)
        data = struct.pack(">II", unk, count)
        for circle, extra_info in circles:
            data += circle.pack()
            data += pati.pack_extra_info(extra_info)
        self.send_packet(PatID4.AnsCircleListLayer, data, seq)

    def recvReqCircleCreate(self, packet_id, data, seq):
        """ReqCircleCreate packet.

        ID: 65010100
        JP: サークル作成要求
        TR: Circle creation request
        """
        circle_info = pati.CircleInfo.unpack(data)
        circle_extra_info = pati.unpack_extra_info(data,
                                                   len(circle_info.pack()))
        # Extra fields
        #  - field_id 0x01: Party capacity
        #  - field_id 0x02: Quest ID
        self.server.debug("CircleCreate: {!r}, {!r}".format(circle_info,
                                                            circle_extra_info))

        city = self.session.get_city()
        (circle, circle_index) = city.get_first_empty_circle()

        assert circle is not None  # TODO:Transmit error when no slot available

        circle.leader = self.session
        circle.players.append(self.session)

        self.session.join_circle(circle_index)

        if "password" in circle_info:
            circle.password = pati.unpack_string(circle_info.password)

        if "remarks" in circle_info:
            circle.remarks = pati.unpack_string(circle_info.remarks)

        circle.capacity = pati.unpack_long(circle_info.team_size)

        for field_id, value in circle_extra_info:
            if field_id == 0x02:  # QuestId
                circle.questId = value

        assert circle.questId >= 10000  # Game's quest id minimum

        circle_info.index = pati.Long(circle_index + 1)
        circle_info.unk_long_0x07 = pati.Long(2)
        circle_info.unk_long_0x08 = pati.Long(3)
        circle_info.team_size = pati.Long(circle.get_capacity())
        circle_info.unk_long_0x0a = pati.Long(5)
        circle_info.unk_long_0x0b = pati.Long(6)
        circle_info.unk_long_0x0c =\
            pati.Long(circle_index + 1)  # TODO: RE what exactly is this field
        circle_info.leader_capcom_id = pati.String(self.session.capcom_id)
        circle_info.unk_byte_0x0f = pati.Byte(0)  # Is Full? VERIFY this

        # Notify every city's player
        ntc_circle_list_layer_create_data = struct.pack(">I", circle_index + 1)
        ntc_circle_list_layer_create_data += circle_info.pack()
        ntc_circle_list_layer_create_data +=\
            pati.pack_extra_info(circle_extra_info)

        for city_player in city.players:
            city_player_handler = self.server.get_pat_handler(city_player)
            city_player_handler.send_packet(PatID4.NtcCircleListLayerCreate,
                                            ntc_circle_list_layer_create_data,
                                            seq)

        self.sendAnsCircleCreate(circle_index + 1, circle_extra_info, seq)

    def sendAnsCircleCreate(self, circle, extra, seq):
        """AnsCircleCreate packet.

        ID: 65010200
        JP: サークル作成返答
        TR: Circle creation response
        """
        data = struct.pack(">I", circle)

        self.send_packet(PatID4.AnsCircleCreate, data, seq)

    def recvReqCircleMatchOptionSet(self, packet_id, data, seq):
        """ReqCircleMatchOptionSet packet.

        ID: 65100100
        JP: マッチングオプション設定要求
        TR: Match option settings request
        """
        options = pati.CircleUserData.unpack(data)
        self.server.debug("MatchOptionSet: {!r}".format(options))
        self.sendAnsCircleMatchOptionSet(options, seq)

    def sendAnsCircleMatchOptionSet(self, options, seq):
        """AnsCircleMatchOptionSet packet.

        ID: 65100200
        JP: マッチングオプション設定返答
        TR: Match option settings response
        """

        circle = self.session.get_circle()
        options.capcom_id = pati.String(self.session.capcom_id)
        options.hunter_name = pati.String(self.session.hunter_name)
        options.player_index = pati.Byte(circle.players.index(self.
                                                              session) + 1)
        ntc_data = options.pack()

        for circle_player in circle.players:
            if circle_player == self.session:
                continue

            pat_handler = self.server.get_pat_handler(circle_player)
            pat_handler.send_packet(PatID4.NtcCircleMatchOptionSet,
                                    ntc_data, seq)

        self.send_packet(PatID4.AnsCircleMatchOptionSet, b"", seq)

    def recvReqCircleInfo(self, packet_id, data, seq):
        """ReqCircleInfo packet.

        ID: 65020100
        JP: サークルデータ取得要求
        TR: Get circle data request
        """
        circle_index, = struct.unpack_from(">I", data)
        unk2 = data[4:4 + 0xd]
        unk3 = data[4 + 0xd:]
        self.server.debug("ReqCircleInfo: {}, {!r}, {!r}".format(
            circle_index, unk2, unk3))
        self.sendAnsCircleInfo(circle_index, unk2, unk3, seq)

    def sendAnsCircleInfo(self, circle_index, unk2, unk3, seq):
        """AnsCircleInfo packet.

        ID: 65020200
        JP: サークルデータ取得返答
        TR: Get circle data response
        """

        data = struct.pack(">I", circle_index)

        city = self.session.get_city()

        # TODO: Verify circle index
        circle = city.circles[circle_index - 1]

        circle_info = pati.CircleInfo()
        circle_info.index = pati.Long(circle_index)
        # circle_info.unk_string_0x02 = pati.String("192.168.23.1")
        if circle.has_password():
            circle_info.has_password = pati.Byte(1)
            circle_info.password = pati.String(circle.password)
        else:
            circle_info.has_password = pati.Byte(0)

        # TODO: Do party member field
        # circle_info.unk_binary_0x05 = pati.Binary([])

        if circle.remarks is not None:
            circle_info.remarks = pati.String(circle.remarks)

        # circle_info.unk_long_0x07 = pati.Long(1)
        # circle_info.unk_long_0x08 = pati.Long(0)

        circle_info.team_size = pati.Long(circle.capacity)

        # circle_info.unk_long_0x0a = pati.Long(1)
        # circle_info.unk_long_0x0b = pati.Long(1)

        extra_info = []
        extra_info.append((1, circle.get_population()))
        extra_info.append((2, circle.questId))

        self.server.debug("AnsCircleInfo: {!r} {!r}".format(circle_info,
                                                            extra_info))

        data += circle_info.pack()
        data += pati.pack_extra_info(extra_info)

        self.send_packet(PatID4.AnsCircleInfo, data, seq)
        # self.send_packet(PatID4.NtcCircleInfoSet, data, seq)

    def recvReqCircleJoin(self, packet_id, data, seq):
        circle_index, = struct.unpack_from(">I", data)

        # In this circle info, the only possible field filled are the:
        # unk_long_0x0b, has_password, password
        circle_info = pati.CircleInfo.unpack(data, 4)

        city = self.session.get_city()

        # TODO: Error out, gracefully
        assert (circle_index - 1) < len(city.circles)

        circle = city.circles[circle_index - 1]

        if circle.get_population() >= circle.get_capacity():
            self.sendAnsCircleJoin(0, 0, seq)
            return

        circle.players.append(self.session)
        self.session.join_circle(circle_index - 1)

        # TODO: Figure out what exactly is this value suppose to do
        unk = circle.get_population()  # This value is suppose to be a byte

        self.sendAnsCircleJoin(circle_index, unk, seq)

    def sendAnsCircleJoin(self, circle_index, unk, seq):
        """AnsCircleJoin packet.

        ID: 65040200
        JP: サークルイン返答
        TR: Circle-in reply
        """

        data = struct.pack(">IB", circle_index, unk)
        self.send_packet(PatID4.AnsCircleJoin, data, seq)

        if circle_index > 0:
            city = self.session.get_city()
            circle = city.circles[circle_index - 1]
            ntc_circle_join_data = struct.pack(">I", circle_index)
            ntc_circle_join_data += pati.lp2_string(self.session.capcom_id)
            ntc_circle_join_data += pati.lp2_string(self.session.hunter_name)
            # TODO NEED RE
            unk1 = circle.get_population()  # NOTE: act as player index
            unk2 = 0

            ntc_circle_join_data += struct.pack(">BB", unk1, unk2)

            for circle_player in circle.players:
                if circle_player == self.session:
                    continue

                circle_player_pat_handler =\
                    self.server.get_pat_handler(circle_player)
                circle_player_pat_handler.send_packet(PatID4.NtcCircleJoin,
                                                      ntc_circle_join_data,
                                                      seq)

    def recvReqCircleUserList(self, packet_id, data, seq):
        """AnsCircleJoin packet.

        ID: 65600100
        JP: サークル同期ユーザリスト要求
        TR: Circle sync user list request
        """
        # Ignore packet data
        self.sendAnsCircleUserList(seq)

    def sendAnsCircleUserList(self, seq):
        """AnsCircleJoin packet.

        ID: 65600200
        JP: サークル同期ユーザリスト返答
        TR: Circle sync user list reply
        """
        circle = self.session.get_circle()

        data = struct.pack(">I", circle.get_population())
        for i, circle_player in enumerate(circle.players):
            circle_user_data = pati.CircleUserData()
            circle_user_data.is_standby = pati.Byte(0)
            circle_user_data.player_index = pati.Byte(i + 1)
            circle_user_data.capcom_id = pati.String(circle_player.capcom_id)
            circle_user_data.hunter_name = pati.String(circle_player.
                                                       hunter_name)
            data += circle_user_data.pack()

        self.send_packet(PatID4.AnsCircleUserList, data, seq)

    def recvReqCircleHost(self, packet_id, data, seq):
        """ReqCircleHost packet.

        ID: 65410100
        JP: サークルのホスト者要求
        TR: Circle host request
        """
        circle_index, = struct.unpack_from(">I", data)
        self.sendAnsCircleHost(circle_index, seq)

    def sendAnsCircleHost(self, circle_index, seq):
        """AnsCircleHost packet.

        ID: 65410100
        JP: サークルのホスト者返答
        TR: Circle host response
        """
        city = self.session.get_city()
        circle = city.circles[circle_index - 1]

        # next(i for i in range(0, circle.get_population())
        #   if circle.players[i] == circle.leader)
        leader_index = 0
        assert leader_index is not None

        # TODO: Verify this field
        unk1 = leader_index + 1

        data = struct.pack(">IB", circle_index, unk1)
        data += pati.lp2_string(circle.leader.capcom_id)
        data += pati.lp2_string(circle.leader.hunter_name)

        for circle_player in circle.players:
            if circle_player == self.session:
                continue

            circle_player_pat_handler =\
                self.server.get_pat_handler(circle_player)
            circle_player_pat_handler.send_packet(PatID4.NtcCircleHost,
                                                  data, seq)

        self.send_packet(PatID4.AnsCircleHost, data, seq)

    def recvNtcCircleBinary(self, packet_id, data, seq):
        circle_index, = struct.unpack_from(">I", data)
        sender_blank = pati.LayerUserInfo.unpack(data, 4)
        unk_data = data[len(sender_blank.pack()) + 4:]
        self.sendNtcCircleBinary(circle_index, unk_data, seq)

    def sendNtcCircleBinary(self, circle_index, unk_data, seq):
        sender = pati.LayerBinaryInfo()
        sender.unk_long_0x01 = pati.Long(0x12345678)
        sender.capcom_id = pati.String(self.session.capcom_id)
        sender.hunter_name = pati.String(self.session.hunter_name)

        self.server.debug("NtcCircleBinary: From ({}, {})"
                          .format(self.session.capcom_id,
                                  self.session.hunter_name))

        data = struct.pack(">I", circle_index)
        data += pati.lp2_string(self.session.capcom_id)
        data += sender.pack()
        data += unk_data

        city = self.session.get_city()
        circle = city.circles[circle_index - 1]
        for circle_player in circle.players:
            if circle_player == self.session:
                continue

            player_pat_handler = self.server.get_pat_handler(circle_player)
            if player_pat_handler is None:
                continue

            player_pat_handler.send_packet(PatID4.NtcCircleBinary, data, seq)

    def recvNtcCircleBinary2(self, packet_id, data, seq):
        circle_index, = struct.unpack_from(">I", data)
        partner = pati.unpack_lp2_string(data, 4)
        partner_size = len(partner) + 2 + 4
        binary_info = pati.LayerBinaryInfo.unpack(data, partner_size)
        unk_data = data[partner_size + len(binary_info.pack()):]

        self.server.debug("NtcCircleBinary2: From ({}, {})\n{}"
                          .format(self.session.capcom_id,
                                  self.session.hunter_name,
                                  hexdump(unk_data)))

        self.sendNtcCircleBinary2(circle_index, partner, unk_data, seq)

    def sendNtcCircleBinary2(self, circle_index, partner, unk_data, seq):
        city = self.session.get_city()
        circle = city.circles[circle_index - 1]
        partner_session = next(p for p in circle.players
                               if p.capcom_id == partner)
        if partner_session is None:
            return

        data = struct.pack(">I", circle_index)
        data += pati.lp2_string(self.session.capcom_id)

        self_data = pati.LayerBinaryInfo()
        self_data.capcom_id = pati.String(self.session.capcom_id)
        self_data.hunter_name = pati.String(self.session.hunter_name)

        data += self_data.pack()
        data += unk_data

        partner_pat_handler = self.server.get_pat_handler(partner_session)
        if partner_pat_handler is None:
            return

        partner_pat_handler.send_packet(PatID4.NtcCircleBinary2, data, seq)

    def recvReqCircleLeave(self, packet_id, data, seq):
        """ReqCircleLeave packet.

        ID: 65030200
        JP: サークルアウト要求
        TR: Circle-in reply
        """
        circle_index, = struct.unpack(">I", data)
        self.sendAnsCircleLeave(circle_index, seq)

    def sendAnsCircleLeave(self, circle_index, seq):
        """AnsCircleLeave packet.

        ID: 65040200
        JP: サークルアウト返答
        TR: Circle out response
        """

        data = struct.pack(">I", circle_index)
        self.send_packet(PatID4.AnsCircleLeave, data, seq)

    def recvReqCircleInfoSet(self, packet_id, data, seq):
        """ReqCircleInfoSet packet.

        ID: 65200100
        JP: サークルデータ設定要求
        TR: Circle data settings request
        """
        circle_index, = struct.unpack_from(">I", data)
        offset = 4
        circle = pati.CircleInfo.unpack(data, offset)
        offset += len(circle.pack())
        extra = pati.unpack_extra_info(data, offset)
        self.server.debug("ReqCircleInfoSet: Circle({}) {!r}, {!r}".format(
            circle_index, circle, extra))
        self.sendAnsCircleInfoSet(circle_index, circle, extra, seq)

    def sendAnsCircleInfoSet(self, circle_index, circle, extra, seq):
        """AnsCircleInfoSet packet.

        ID: 65040200
        JP: サークルデータ設定返答
        TR: Circle data settings response
        """

        ntc_data = struct.pack(">I", circle_index)
        ntc_data += circle.pack()
        ntc_data += pati.pack_extra_info(extra)

        city = self.session.get_city()
        circle = city.circles[circle_index - 1]

        for circle_player in circle.players:
            if circle_player == self.session:
                continue

            circle_player_pat_handler =\
                self.server.get_pat_handler(circle_player)
            circle_player_pat_handler.send_packet(PatID4.NtcCircleInfoSet,
                                                  ntc_data, seq)

        data = struct.pack(">I", circle_index)
        self.send_packet(PatID4.AnsCircleInfoSet, data, seq)

    def recvReqCircleMatchStart(self, packet_id, data, seq):
        """ReqCircleMatchStart packet.

        ID: 65120100
        JP: マッチング開始要求
        TR: Matching start request
        """
        self.sendAnsCircleMatchStart(seq)

    def sendAnsCircleMatchStart(self, seq):
        """AnsCircleMatchStart packet.

        ID: 65120200
        JP: マッチング開始返答
        TR: Matching start response
        """

        self.sendNtcCircleMatchStart(seq)
        self.send_packet(PatID4.AnsCircleMatchStart, b"", seq)

    def sendNtcCircleMatchStart(self, seq):
        """NtcCircleMatchStart packet.

        ID: 65121000
        JP: マッチング開始通知
        TR: Matching start notification
        """

        circle = self.session.get_circle()

        count = circle.get_population()
        data = struct.pack(">I", count)
        i = 0
        for circle_player in circle.players:
            data += struct.pack(">B", i + 1)
            data += pati.lp2_string(circle_player.capcom_id)
            data += pati.lp2_string(b"\1")
            data += struct.pack(">H", 21)  # TODO: Field??
            i += 1
        data = struct.pack(">H", len(data)) + data
        data += struct.pack(">I", 1)  # Field??

        for circle_player in circle.players:
            pat_handler = self.server.get_pat_handler(circle_player)
            pat_handler.send_packet(PatID4.NtcCircleMatchStart, data, seq)

    def recvReqCircleMatchEnd(self, packet_id, data, seq):
        """ReqCircleMatchEnd packet.

        ID: 65130100
        JP: マッチング終了要求
        TR: Matching end request
        """
        self.sendAnsCircleMatchEnd(seq)

    def sendAnsCircleMatchEnd(self, seq):
        """AnsCircleMatchEnd packet.

        ID: 65130200
        JP: マッチング終了返答
        TR: Matching end notification
        """
        self.send_packet(PatID4.AnsCircleMatchEnd, b"", seq)


BASE = server_base("FMP", FmpServer, FmpRequestHandler)

if __name__ == "__main__":
    server_main(*BASE)
