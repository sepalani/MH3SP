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

from mh.database import Players
import mh.pat_item as pati
from mh.constants import *
from mh.pat import PatRequestHandler, PatServer
from other.utils import hexdump, server_base, server_main


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
            self.server.layer_broadcast(self.session, PatID4.NtcLayerIn,
                                        data, seq)

        data = struct.pack(">H", layer_id)
        self.send_packet(PatID4.AnsLayerDown, data, seq)

    def recvReqUserBinarySet(self, packet_id, data, seq):
        """ReqUserBinarySet packet.

        ID: 66310100
        JP: ユーザ表示用バイナリ設定要求
        TR: Binary setting request for user display

        The game sends the updated user display binary settings to the server.

        Examples:
         - Online > Settings > Profile
         - Online > Settings > Status Indicator
        """
        offset, length = struct.unpack_from(">IH", data)
        binary = pati.unpack_lp2_string(data, 4)
        self.session.hunter_info.unpack(data[6:], length, offset)

        self.sendAnsUserBinarySet(offset, binary, seq)

    def sendAnsUserBinarySet(self, unk1, profile_info, seq):
        """AnsUserBinarySet packet.

        ID: 66310200
        JP: ユーザ表示用バイナリ設定返答
        TR: Binary setting reply for user display

        TODO: Properly handle binary settings.
        """
        self.send_packet(PatID4.AnsUserBinarySet, b"", seq)

    def recvReqUserBinaryNotice(self, packet_id, data, seq):
        """ReqUserBinaryNotice packet.

        ID: 66320100
        JP: ユーザ表示用バイナリ通知要求
        TR: Binary notification request for user display
        """
        unk1, = struct.unpack_from(">B", data)
        capcom_id = pati.unpack_lp2_string(data, 1)
        offset, length = struct.unpack_from(">II", data, 3+len(capcom_id))
        self.sendAnsUserBinaryNotice(unk1, capcom_id, offset, length, seq)

    def sendAnsUserBinaryNotice(self, unk1, capcom_id, offset, length, seq):
        """AnsUserBinaryNotice packet.

        ID: 66320200
        JP: ユーザ表示用バイナリ通知返答
        TR: Binary notification reply for user display
        """
        data = struct.pack(">B", unk1)
        data += pati.lp2_string(self.session.capcom_id)
        data += struct.pack(">I", 0)
        data += pati.lp2_string(self.session.hunter_info.pack())
        self.server.layer_broadcast(self.session, PatID4.NtcUserBinaryNotice,
                                    data, seq)
        self.send_packet(PatID4.AnsUserBinaryNotice, b"", seq)

    def recvReqLayerUserList(self, packet_id, data, seq):
        """ReqLayerUserList packet.

        ID: 64630100
        JP: レイヤ同期ユーザリスト要求
        TR: Layer sync user list request
        """
        count, = struct.unpack_from(">B", data)
        unk = struct.unpack_from(">"+count * "B", data, 1)
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

        for _, player in players:
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

        self.server.debug("ReqLayerHost: Req ({}, {})  Host ({}, {})".format(
            self.session.capcom_id, self.session.hunter_name,
            leader.capcom_id, leader.hunter_name))

        data = unk_data
        data += pati.lp2_string(leader.capcom_id)
        data += pati.lp2_string(leader.hunter_name)
        self.send_packet(PatID4.AnsLayerHost, data, seq)

        # Notify the city's players of the new player
        user = pati.LayerUserInfo()
        user.capcom_id = pati.String(self.session.capcom_id)
        user.hunter_name = pati.String(self.session.hunter_name)
        user.stats = pati.Binary(self.session.hunter_info.pack())

        data = pati.lp2_string(self.session.capcom_id)
        data += user.pack()

        self.server.layer_broadcast(self.session, PatID4.NtcLayerIn,
                                    data, seq)

    def recvNtcLayerUserPosition(self, packet_id, data, seq):
        """NtcLayerUserPosition packet.

        ID: 64711000
        JP: レイヤゲームポジション受信通知
        TR: Layer game position reception notification
        """
        self.sendNtcLayerUserPosition(data, seq)

    def sendNtcLayerUserPosition(self, fo, seq):
        """NtcLayerUserPosition packet.

        ID: 64711000
        JP: レイヤゲームポジション通知
        TR: Layer game position notification
        """
        data = pati.lp2_string(self.session.capcom_id)
        data += fo
        self.server.layer_broadcast(self.session, PatID4.NtcLayerUserPosition,
                                    data, seq)

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

        self.server.debug("NtcLayerBinary: From ({}, {})".format(
            self.session.capcom_id, self.session.hunter_name))

        data = pati.lp2_string(self.session.capcom_id)
        data += sender.pack()
        data += unk_data

        self.server.layer_broadcast(self.session, PatID4.NtcLayerBinary,
                                    data, seq)

    def recvNtcLayerBinary2(self, packet_id, data, seq):
        """NtcLayerBinary packet.

        ID: 64751000
        JP: レイヤユーザ用バイナリ通知 (相手指定)
        TR: Binary notification for layer users (specify the other party)
        """
        partner = pati.unpack_lp2_string(data)
        partner_size = len(partner) + 2
        binary_info = pati.LayerBinaryInfo.unpack(data, partner_size)
        unk_data = data[partner_size+len(binary_info.pack()):]

        self.server.debug("NtcLayerBinary2: From ({}, {})\n{}".format(
            self.session.capcom_id, self.session.hunter_name,
            hexdump(unk_data)))
        self.sendNtcLayerBinary2(partner, unk_data, seq)

    def sendNtcLayerBinary2(self, partner, unk_data, seq):
        """NtcLayerBinary packet.

        ID: 64751000
        JP: レイヤユーザ用バイナリ通知 (相手指定)
        TR: Binary transmission for layer users (specify the other party)
        """
        city = self.session.get_city()
        partner_session = city.players.find_by_capcom_id(partner)
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
            self.server.layer_broadcast(self.session, PatID4.NtcLayerOut,
                                        ntc_data, seq)
        self.sendAnsLayerUp(data, seq)

    def recvReqUserSearchInfoMine(self, packet_id, data, seq):
        """ReqUserSearchInfoMine packet.

        ID: 66370100
        JP: ユーザ検索データ要求(自分)
        TR: User search data request (self)
        """
        search_info = pati.UserSearchInfo.unpack(data)
        self.server.debug("SearchInfo: {!r}".format(search_info))
        self.sendAnsUserSearchInfoMine(search_info, seq)

    def sendAnsUserSearchInfoMine(self, search_info, seq):
        """AnsUserSearchInfoMine packet.

        ID: 66370200
        JP: ユーザ検索データ返答(自分)
        TR: User search data reply (self)

        TODO: Figure out what to do with it.
        Maybe prevent the same profile to be connected twice simultaneously.
        """
        info_mine_0x0f = int(hash(self.session.capcom_id)) & 0xffffffff
        info_mine_0x10 = int(hash(self.session.capcom_id[::-1])) & 0xffffffff

        self.server.debug("SearchInfoMine: {:08X} {:08X}".format(
            info_mine_0x0f, info_mine_0x10))

        search_info = pati.UserSearchInfo()

        # This fields are used to identify a user.
        # Specifically when a client is deserializing data from the packets
        # `NtcLayerBinary` and `NtcLayerBinary2`
        # TODO: Proper field value and name
        search_info.info_mine_0x0f = pati.Long(info_mine_0x0f)
        search_info.info_mine_0x10 = pati.Long(info_mine_0x10)
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

        city = self.session.get_city()

        unk = 0
        count = 0

        data = b''
        for i, circle in enumerate(city.circles):
            if not circle.is_empty():
                data += pati.CircleInfo.pack_from(circle, i+1)
                count += 1

        data = struct.pack(">II", unk, count) + data

        self.send_packet(PatID4.AnsCircleListLayer, data, seq)

    def recvReqCircleCreate(self, packet_id, data, seq):
        """ReqCircleCreate packet.

        ID: 65010100
        JP: サークル作成要求
        TR: Circle creation request
        """
        circle_info = pati.CircleInfo.unpack(data)
        circle_optional_fields = pati.unpack_optional_fields(
            data, len(circle_info.pack()))
        self.server.debug("CircleCreate: {!r}, {!r}".format(
                          circle_info, circle_optional_fields))

        city = self.session.get_city()
        circle, circle_index = city.get_first_empty_circle()

        # TODO: Transmit error when no slot available
        assert circle is not None, "No Empty Circle Found"

        circle.leader = self.session

        if "password" in circle_info:
            circle.password = pati.unpack_string(circle_info.password)

        if "remarks" in circle_info:
            circle.remarks = pati.unpack_string(circle_info.remarks)

        if "unk_byte_0x0e" in circle_info:
            circle.unk_byte_0x0e = pati.unpack_byte(circle_info.unk_byte_0x0e)

        circle.players = Players(pati.unpack_long(circle_info.capacity))
        circle.players.add(self.session)

        self.session.join_circle(circle_index)

        # Extra fields
        #  - field_id 0x01: Party capacity
        #  - field_id 0x02: Quest ID
        for field_id, value in circle_optional_fields:
            if field_id == 0x02:  # QuestId
                circle.quest_id = value

        assert circle.quest_id >= 10000  # Game's quest id minimum

        # Notify every city's player
        self.sendNtcCircleListLayerChange(circle, circle_index + 1, seq)

        self.sendAnsCircleCreate(circle_index+1, seq)

    def sendAnsCircleCreate(self, circle_index, seq):
        """AnsCircleCreate packet.

        ID: 65010200
        JP: サークル作成返答
        TR: Circle creation response
        """
        data = struct.pack(">I", circle_index)
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

        is_standby = 'is_standby' in options and \
            pati.unpack_byte(options.is_standby) == 1

        self.session.set_circle_standby(is_standby)

        circle = self.session.get_circle()
        options.capcom_id = pati.String(self.session.capcom_id)
        options.hunter_name = pati.String(self.session.hunter_name)
        options.player_index = pati.Byte(circle.players.index(self.session)+1)
        ntc_data = options.pack()
        self.server.circle_broadcast(circle, PatID4.NtcCircleMatchOptionSet,
                                     ntc_data, seq, self.session)
        self.send_packet(PatID4.AnsCircleMatchOptionSet, b"", seq)

    def recvReqCircleInfo(self, packet_id, data, seq):
        """ReqCircleInfo packet.

        ID: 65020100
        JP: サークルデータ取得要求
        TR: Circle data acquisition request
        """
        circle_index, = struct.unpack_from(">I", data)
        unk2 = data[4:4+0xd]
        unk3 = data[4+0xd:]
        self.server.debug("ReqCircleInfo: {}, {!r}, {!r}".format(
            circle_index, unk2, unk3))
        self.sendAnsCircleInfo(circle_index, unk2, unk3, seq)

    def sendAnsCircleInfo(self, circle_index, unk2, unk3, seq):
        """AnsCircleInfo packet.

        ID: 65020200
        JP: サークルデータ取得返答
        TR: Circle data acquisition reply
        """

        city = self.session.get_city()

        # TODO: Verify circle index
        circle = city.circles[circle_index-1]

        data = struct.pack(">I", circle_index)
        data += pati.CircleInfo.pack_from(circle, circle_index)

        self.send_packet(PatID4.AnsCircleInfo, data, seq)

    def recvReqCircleJoin(self, packet_id, data, seq):
        """ReqCircleJoin packet.

        ID: 65030100
        JP: サークルイン要求
        TR: Circle-in request
        """
        circle_index, = struct.unpack_from(">I", data)

        # In this circle info, the only possible field filled are:
        # unk_long_0x0b, has_password, password
        circle_info = pati.CircleInfo.unpack(data, 4)

        city = self.session.get_city()

        # TODO: Error out, gracefully
        assert (circle_index-1) < len(city.circles)

        circle = city.circles[circle_index-1]

        if circle.has_password() and ("password" not in circle_info or
                                      pati.unpack_string(circle_info.password)
                                      != circle.password):
            self.sendAnsAlert(PatID4.AnsCircleJoin,
                              "<LF=8><BODY><CENTER>Wrong Password!<END>", seq)
            return

        player_index = circle.players.add(self.session)
        if player_index == -1:
            self.sendAnsAlert(PatID4.AnsCircleJoin,
                              "<LF=8><BODY><CENTER>Quest is full!<END>", seq)
            return

        self.session.join_circle(circle_index-1)
        self.sendAnsCircleJoin(circle_index, player_index+1, seq)

    def sendAnsCircleJoin(self, circle_index, player_index, seq):
        """AnsCircleJoin packet.

        ID: 65030200
        JP: サークルイン返答
        TR: Circle-in reply
        """
        assert circle_index > 0 and player_index > 0

        data = struct.pack(">IB", circle_index, player_index)
        self.send_packet(PatID4.AnsCircleJoin, data, seq)

        city = self.session.get_city()
        circle = city.circles[circle_index-1]
        ntc_data = struct.pack(">I", circle_index)
        ntc_data += pati.lp2_string(self.session.capcom_id)
        ntc_data += pati.lp2_string(self.session.hunter_name)

        # If state == 2 it increment a variable on NetworkSessionManagerPat
        state = 0

        ntc_data += struct.pack(">BB", player_index, state)
        self.server.circle_broadcast(circle, PatID4.NtcCircleJoin, ntc_data,
                                     seq, self.session)

    def recvReqCircleUserList(self, packet_id, data, seq):
        """ReqCircleUserList packet.

        ID: 65600100
        JP: サークル同期ユーザリスト要求
        TR: Circle sync user list request
        """
        # Ignore packet data
        self.sendAnsCircleUserList(seq)

    def sendAnsCircleUserList(self, seq):
        """AnsCircleUserList packet.

        ID: 65600200
        JP: サークル同期ユーザリスト返答
        TR: Circle sync user list reply
        """
        circle = self.session.get_circle()

        data = struct.pack(">I", circle.get_population())
        for i, player in circle.players:
            circle_user_data = pati.CircleUserData()
            circle_user_data.is_standby = pati.Byte(
                int(player.is_circle_standby()))
            circle_user_data.player_index = pati.Byte(i+1)
            circle_user_data.capcom_id = pati.String(player.capcom_id)
            circle_user_data.hunter_name = pati.String(player.hunter_name)
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

        ID: 65410200
        JP: サークルのホスト者返答
        TR: Circle host response
        """
        city = self.session.get_city()
        circle = city.circles[circle_index-1]

        leader_index = circle.players.index(circle.leader)
        assert leader_index != -1, "Leader wasn't found"

        data = struct.pack(">IB", circle_index, leader_index+1)
        data += pati.lp2_string(circle.leader.capcom_id)
        data += pati.lp2_string(circle.leader.hunter_name)

        self.send_packet(PatID4.AnsCircleHost, data, seq)

    def recvNtcCircleBinary(self, packet_id, data, seq):
        """NtcCircleBinary packet.

        ID: 65701000
        JP: サークルバイナリ通知
        TR: Circle binary notification
        """
        circle_index, = struct.unpack_from(">I", data)
        sender_blank = pati.LayerUserInfo.unpack(data, 4)
        unk_data = data[len(sender_blank.pack())+4:]
        self.sendNtcCircleBinary(circle_index, unk_data, seq)

    def sendNtcCircleBinary(self, circle_index, unk_data, seq):
        """NtcCircleBinary packet.

        ID: 65701000
        JP: サークルバイナリ送信
        TR: Circle binary transmission
        """
        sender = pati.LayerBinaryInfo()
        sender.unk_long_0x01 = pati.Long(0x12345678)
        sender.capcom_id = pati.String(self.session.capcom_id)
        sender.hunter_name = pati.String(self.session.hunter_name)

        self.server.debug("NtcCircleBinary: From ({}, {})".format(
            self.session.capcom_id, self.session.hunter_name))

        data = struct.pack(">I", circle_index)
        data += pati.lp2_string(self.session.capcom_id)
        data += sender.pack()
        data += unk_data

        city = self.session.get_city()
        circle = city.circles[circle_index-1]
        self.server.circle_broadcast(circle, PatID4.NtcCircleBinary, data,
                                     seq, self.session)

    def recvNtcCircleBinary2(self, packet_id, data, seq):
        """NtcCircleBinary2 packet.

        ID: 65711000
        JP: サークルバイナリ通知 (相手指定)
        TR: Circle binary notification (specified by the other party)
        """
        circle_index, = struct.unpack_from(">I", data)
        partner = pati.unpack_lp2_string(data, 4)
        partner_size = len(partner)+2+4
        binary_info = pati.LayerBinaryInfo.unpack(data, partner_size)
        unk_data = data[partner_size+len(binary_info.pack()):]

        self.server.debug("NtcCircleBinary2: From ({}, {})\n{}".format(
            self.session.capcom_id, self.session.hunter_name,
            hexdump(unk_data)))

        self.sendNtcCircleBinary2(circle_index, partner, unk_data, seq)

    def sendNtcCircleBinary2(self, circle_index, partner, unk_data, seq):
        """NtcCircleBinary2 packet.

        ID: 65711000
        JP: サークルバイナリ送信 (相手指定)
        TR: Circle binary transmission (specified by the other party)
        """
        city = self.session.get_city()
        circle = city.circles[circle_index-1]
        partner_session = circle.players.find_by_capcom_id(partner)
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

        ID: 65040100
        JP: サークルアウト要求
        TR: Circle out request
        """
        circle_index, = struct.unpack(">I", data)
        self.sendAnsCircleLeave(circle_index, seq)

    def sendAnsCircleLeave(self, circle_index, seq):
        """AnsCircleLeave packet.

        ID: 65040200
        JP: サークルアウト返答
        TR: Circle out reply
        """

        circle = self.session.get_circle()

        if circle.leader == self.session:
            self.sendNtcCircleBreak(circle, seq)

        self.session.leave_circle()

        # Delete the quest from the quest board
        self.sendNtcCircleListLayerChange(circle, circle_index, seq)

        data = struct.pack(">I", circle_index)
        self.send_packet(PatID4.AnsCircleLeave, data, seq)

    def sendNtcCircleBreak(self, circle, seq):
        """NtcCircleBreak packet.

        ID: 65051000
        JP: サークル解散通知
        TR: Circle dissolution notice
        """

        # Unknown field but it doesn't matter because the client ignores it
        unk1 = 0

        data = struct.pack(">I", unk1)
        self.server.circle_broadcast(circle, PatID4.NtcCircleBreak, data, seq,
                                     self.session)

    def sendNtcCircleKick(self, circle, seq):
        """NtcCircleKick packet.

        ID: 65351000
        JP: サークルからキック通知
        TR: Kick notification from the circle
        """

        # Unknown field but it doesn't matter because the client ignores them
        unk1 = 0
        unk2 = b""

        data = struct.pack(">B", unk1)
        data += pati.lp2_string(unk2)
        self.server.circle_broadcast(circle, PatID4.NtcCircleKick, data, seq,
                                     self.session)

    def recvReqCircleInfoSet(self, packet_id, data, seq):
        """ReqCircleInfoSet packet.

        ID: 65200100
        JP: サークルデータ設定要求
        TR: Circle data setting request
        """
        circle_index, = struct.unpack_from(">I", data)
        circle_info = pati.CircleInfo.unpack(data, 4)
        offset = 4 + len(circle_info.pack())
        optional_fields = pati.unpack_optional_fields(data, offset)

        self.server.debug("CircleInfo: {!r}".format(circle_info))

        city = self.session.get_city()
        circle = city.circles[circle_index-1]

        self.sendAnsCircleInfoSet(circle_index, circle_info, optional_fields,
                                  seq)

        self.sendNtcCircleListLayerChange(circle, circle_index, seq)

    def sendAnsCircleInfoSet(self, circle_index, circle_info, optional_fields,
                             seq):
        """AnsCircleInfoSet packet.

        ID: 65200200
        JP: サークルデータ設定返答
        TR: Circle data setting reply
        """
        ntc_data = struct.pack(">I", circle_index)
        ntc_data += circle_info.pack()
        ntc_data += pati.pack_optional_fields(optional_fields)

        city = self.session.get_city()
        circle = city.circles[circle_index-1]
        self.server.circle_broadcast(circle, PatID4.NtcCircleInfoSet, ntc_data,
                                     seq, self.session)

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
        TR: Matching start reply
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
        circle.departed = True

        count = 0
        data = b''
        for i, player in circle.players:
            if player.is_circle_standby():
                data += struct.pack(">B", i+1)
                data += pati.lp2_string(player.capcom_id)
                data += pati.lp2_string(b"\1")
                data += struct.pack(">H", 21)  # TODO: Field??
                player.set_in_quest()
                count += 1
            else:
                # Client ignore field
                ntc_circle_kick = struct.pack(">B", 0) + pati.lp2_string('')
                pat_handler = self.server.get_pat_handler(player)
                pat_handler.send_packet(PatID4.NtcCircleKick, ntc_circle_kick,
                                        seq)
                circle.players.remove(i)

        data = struct.pack(">I", count)+data
        data = struct.pack(">H", len(data))+data
        data += struct.pack(">I", 1)  # Field??

        self.server.circle_broadcast(circle, PatID4.NtcCircleMatchStart, data,
                                     seq)

    def recvReqCircleMatchEnd(self, packet_id, data, seq):
        """ReqCircleMatchEnd packet.

        ID: 65130100
        JP: マッチング終了要求
        TR: Matching end request
        """

        unk, = struct.unpack_from(">B", data)
        # unk is a bolean, but is unknown what it represent

        self.sendAnsCircleMatchEnd(seq)

    def sendAnsCircleMatchEnd(self, seq):
        """AnsCircleMatchEnd packet.

        ID: 65130200
        JP: マッチング終了返答
        TR: Matching end reply
        """

        self.send_packet(PatID4.AnsCircleMatchEnd, b"", seq)

    def sendNtcCircleListLayerDelete(self, circle, seq):
        """NtcCircleMatchStart packet.

        ID: 65831000
        JP: サークル削除通知 (レイヤ)
        TR: Circle deletion notification (layer)
        """

        circle_index = circle.parent.circles.index(circle) + 1
        ntc_data = struct.pack(">I", circle_index)
        self.server.layer_broadcast(self.session,
                                    PatID4.NtcCircleListLayerDelete, ntc_data,
                                    seq, False)

    def sendNtcCircleListLayerChange(self, circle, circle_index, seq):
        """NtcCircleListLayerChange packet.

        ID: 65821000
        JP: サークル変更通知 (レイヤ)
        TR: Circle change notification (layer)
        """

        ntc_data = struct.pack(">I", circle_index)
        ntc_data += pati.CircleInfo.pack_from(circle, circle_index)

        self.server.layer_broadcast(self.session,
                                    PatID4.NtcCircleListLayerChange, ntc_data,
                                    seq, False)


BASE = server_base("FMP", FmpServer, FmpRequestHandler)


if __name__ == "__main__":
    server_main(*BASE)
