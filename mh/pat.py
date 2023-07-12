#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2021-2023 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Monster Hunter PAT module."""

import struct
import traceback
from datetime import timedelta

from other.utils import Logger, get_config, get_ip, hexdump, to_str

import mh.pat_item as pati
import mh.server as server
import mh.time_utils as time_utils
from mh.constants import \
    LAYER_CHAT_COLORS, TERMS_VERSION, TERMS, SUBTERMS, ANNOUNCE, \
    CHARGE, VULGARITY_INFO, FMP_VERSION, PAT_BINARIES, PAT_NAMES, PatID4
from mh.session import Session

g_circle = None
g_circle_info_set = None


class PatServer(server.BasicPatServer, Logger):
    """Generic PAT server class."""

    def __init__(self, address, handler_class, max_thread_count=0,
                 logger=None, debug_mode=False):
        server.BasicPatServer.__init__(self, address, handler_class,
                                       max_thread_count)
        Logger.__init__(self)
        if logger:
            self.set_logger(logger)
        self.info("Running on {} port {}".format(*address))
        self.debug_con = []
        self.debug_mode = debug_mode

    def add_to_debug(self, con):
        """Add connection to the debug connection list."""
        self.debug_con.append(con)

    def del_from_debug(self, con):
        """Delete connection from the debug connection list."""
        self.debug_con.remove(con)

    def get_debug(self):
        """Return the debug connection list."""
        return self.debug_con

    def debug_enabled(self):
        return self.debug_mode

    def get_pat_handler(self, session):
        """Return pat handler from session"""
        for handler in self.debug_con:
            if handler.session == session:
                return handler

        return None

    def broadcast(self, players, packet_id, data, seq, to_exclude=None):
        # type: (db.Players, int, bytes, int, Session|None) -> None
        handlers = []
        with players.lock():
            for _, player in players:
                if player == to_exclude:
                    continue

                handler = self.get_pat_handler(player)
                if handler:
                    handlers.append(handler)
        for handler in handlers:
            handler.try_send_packet(packet_id, data, seq)

    def layer_broadcast(self, session, packet_id, data, seq,
                        exclude_self=True):
        # type: (Session, int, bytes, int, bool) -> None
        self.broadcast(session.get_layer_players(), packet_id, data, seq, 
                       session if exclude_self else None)

    def circle_broadcast(self, circle, packet_id, data, seq,
                         session=None):
        # type: (db.Circle, int, bytes, int, Session|None) -> None
        self.broadcast(circle.players, packet_id, data, seq, session)
            


class PatRequestHandler(server.BasicPatHandler):
    """Generic PAT request handler class.

    When possible, each packet is described with:
     - ID: Packet ID (in hexadecimal)
     - JP: Japanese description from the game's packet table
     - TR: A roughly translated description

    At some point, I'll add packet hexdumps and description for
    a better understanding. All descriptions are provided with
    the best of our understanding of the packets and might be
    inaccurate. `unk` stands for `unknown`.
    """

    def on_init(self):
        """Default PAT handler."""
        self.server.info("Handle client from {}".format(self.client_address))
        self.server.add_to_debug(self)
        self.session = Session(self)
        self.ping_timer = time_utils.Timer()
        self.requested_connection = False
        self.line_check = True

    def try_send_packet(self, packet_id=0, data=b'', seq=0):
        """Send PAT packet and catch exceptions."""
        try:
            self.send_packet(packet_id, data, seq)
        except Exception:
            self.server.warning(
                "Failed to send %s[ID=%08x; Seq=%04x]\n%s\n%s",
                PAT_NAMES.get(packet_id, "Packet"),
                packet_id, seq, traceback.format_exc(), hexdump(data)
            )

    def try_send_packet_to(self, capcom_id, packet_id=0, data=b'', seq=0):
        """Send PAT packet to specific Capcom ID and catch exceptions."""
        session = self.session.find_user_by_capcom_id(capcom_id)
        if not session:
            self.server.warning("Failed to send packet to %s: user not found",
                                capcom_id)
            return
        handler = self.server.get_pat_handler(session)
        if handler:
            handler.try_send_packet(packet_id, data, seq)

    def sendAnsNg(self, packet_id, message, seq):
        unk1 = 1  # If value is 0, the message is not rendered
        data = struct.pack(">I", unk1)
        data += pati.lp2_string(message)

        packet_id = packet_id | 0xff
        self.send_packet(packet_id, data, seq)

    def sendAnsAlert(self, packet_id, message, seq):
        unk1 = 1  # If value is 0, the message is not rendered
        data = struct.pack(">I", unk1)
        data += pati.lp2_string(message)

        packet_id = packet_id | 0x01
        self.send_packet(packet_id, data, seq)

    def send_error(self, message, seq=0):
        """Send an error message."""
        try:
            MAX_SIZE = 0x200
            MAX_WIDTH = 55
            MAX_HEIGHT = 15
            LINE_PER_PAGE = min(MAX_HEIGHT, MAX_SIZE // MAX_WIDTH)

            lines = [
                "<LF=2><BODY><CENTER>A communication error occurred",
                "<BR><BODY>Check the server log files for more details",
                "<BR><LEFT>",
            ] + message.replace("\\", "/").split("\n")

            def range_slice(obj, chunk_size):
                """Range helper."""
                length = len(obj)
                return range(length // chunk_size + (length % chunk_size > 0))

            def helper(line):
                """Split lines helper."""
                if len(line) <= MAX_WIDTH:
                    return [line]
                return [
                    line[i*MAX_WIDTH:(i+1)*MAX_WIDTH]
                    for i in range_slice(line, MAX_WIDTH)
                ]
            # Flatten the results
            lines = sum([helper(line) for line in lines], [])

            for i in range_slice(lines, LINE_PER_PAGE):
                seq += 1
                message = "<BR><BODY>".join(lines[i*LINE_PER_PAGE:
                                                  (i+1)*LINE_PER_PAGE])
                # It seems we can't send multiple messages
                # self.sendNtcShut("<LF=2><BODY>"+message+"<END>", seq)
                self.sendNtcShut(message + "<END>", 0)
                # The game will close the connection and the next messages
                # won't be received. The except block will be reached if the
                # message is too long.
        except Exception:
            # Probably unreachable and was disconnected
            self.server.warning("Failed to send a complete error message")
        finally:
            self.session.request_reconnection = False
            self.finish()

    def recvNtcCollectionLog(self, packet_id, data, seq):
        """NtcCollectionLog packet.

        ID: 60501000
        JP: 収集ログ通知
        TR: Collection log notification

        This packet is sent by the game when an error occurs.

        TODO: Find all error codes and their meanings.

        Error codes:
         - 0x80050037: Unable to find CircleListLayer Slot
         - 0x80060002: Fail to warp to location (Layer index error?)
         - 0x80070002: Empty NetworkUniqueId?
        """
        data = pati.CollectionLog.unpack(data)
        self.server.debug("CollectionLog: {!r}".format(data))

    def sendReqLineCheck(self):
        """ReqLineCheck packet.

        ID: 60010100
        JP: ラインチェック
        TR: Line check

        The server sends a request to check if the player is still online.
        The game will close the connection after 90s, if it doesn't receive it.
        """
        self.send_packet(PatID4.ReqLineCheck)

    def recvAnsLineCheck(self, packet_id, data, seq):
        """AnsLineCheck packet.

        ID: 60010200
        JP: ラインチェック
        TR: Line check

        The game sends this packet after receiving a ReqLineCheck packet.
        """
        self.line_check = True

    def sendReqConnection(self, unused=0, seq=0):
        """ReqConnection packet.

        ID: 60200100
        JP: ＰＡＴ接続環境要求
        TR: PAT connection settings request

        The server sends a request to the game to establish a PAT connection.
        It also sends a parameter that seems unused on the western versions.
        """
        data = struct.pack(">I", unused)
        self.send_packet(PatID4.ReqConnection, data, seq)

    def recvAnsConnection(self, packet_id, data, seq):
        """AnsConnection packet.

        ID: 60200200
        JP: ＰＡＴ接続環境返答
        TR: PAT connection settings response

        The games sends the PAT environment properties.
        """
        settings = pati.ConnectionData.unpack(data)
        self.server.debug("Connection: {!r}".format(settings))
        pat_ticket = b""
        if "pat_ticket" in settings:
            _, pat_ticket = pati.unpack_any(settings.pat_ticket)
        elif "online_support_code" in settings:
            _, pat_ticket = pati.unpack_any(settings.online_support_code)
        self.server.info("Client {} Ticket `{}`".format(self.client_address,
                                                        pat_ticket))
        self.sendNtcLogin(5, settings, seq)

    def sendNtcLogin(self, server_status, connection_data, seq):
        """NtcLogin packet.

        ID: 60211000
        JP: ログイン処理概要通知
        TR: Login process summary notification

        The server sends upon login a notification with the server status.
        """
        data = struct.pack(">B", server_status)
        self.session = self.session.get(connection_data)
        self.send_packet(PatID4.NtcLogin, data, seq)

    def recvReqAuthenticationToken(self, packet_id, data, seq):
        """ReqAuthenticationToken packet.

        ID: 62600100
        JP: 認証トークン送信
        TR: Send authentication token

        The games requests a PAT authentication by forwarding the token
        obtained from Nintendo NAS server.
        """
        nas_token = pati.unpack_lp2_string(data)
        self.server.info("Client {} - NAS `{}`".format(self.client_address,
                                                       nas_token))
        self.sendAnsAuthenticationToken(nas_token, seq)

    def sendAnsAuthenticationToken(self, nas_token, seq):
        """AnsAuthenticationToken packet.

        ID: 62600200
        JP: 認証トークン返答
        TR: Authentication token response

        The server replies this packet to acknowledge the authentication.
        """
        self.send_packet(PatID4.AnsAuthenticationToken, b'', seq)

    def recvReqTermsVersion(self, packet_id, data, seq):
        """ReqTermsVersion packet.

        ID: 62100100
        JP: 利用規約情報確認
        TR: Terms of use information verification

        The game requests the terms version and its total size.
        """
        self.sendAnsTermsVersion(TERMS_VERSION, len(TERMS[TERMS_VERSION]), seq)

    def sendAnsTermsVersion(self, terms_version, terms_size, seq):
        """AnsTermsVersion packet.

        ID: 62100200
        JP: 利用規約情報応答
        TR: Terms of use information response

        The server replies with the terms version and total size.
        """
        data = struct.pack(">II", terms_version, terms_size)
        self.send_packet(PatID4.AnsTermsVersion, data, seq)

    def recvReqTerms(self, packet_id, data, seq):
        """ReqTerms packet.

        ID: 62110100
        JP: 利用規約要求
        TR: Terms of use request

        The game requests the terms based on what it has already read.
        """
        version, offset, size = struct.unpack(">III", data)
        self.sendAnsTerms(offset, size, TERMS[version], seq)

    def sendAnsTerms(self, offset, size, terms, seq):
        """AnsTerms packet.

        ID: 62110200
        JP: 利用規約応答
        TR: Terms of use response

        The server replies with the terms offset, size and chunk requested.
        """
        data = struct.pack(">II", offset, size)
        data += pati.lp2_string(terms[offset:offset+size])
        self.send_packet(PatID4.AnsTerms, data, seq)

    def recvReqSubTermsInfo(self, packet_id, data, seq):
        """ReqSubTermsInfo european packet.

        ID: 62130100
        JP: サブ利用規約指定情報確認
        TR: Sub-terms of use information verification

        The game requests the sub-terms info.
        """
        unk, = struct.unpack(">B", data)
        self.sendAnsSubTermsInfo(unk, len(SUBTERMS[TERMS_VERSION]), seq)

    def sendAnsSubTermsInfo(self, unk, size, seq):
        """AnsSubTermsInfo european packet.

        ID: 62130200
        JP: サブ利用規約指定情報応答
        TR: Sub-terms of use information response

        The server acknowledges the request.
        """
        unk1 = 1
        data = struct.pack(">IBI", unk1, unk, size)
        self.send_packet(PatID4.AnsSubTermsInfo, data, seq)

    def recvReqSubTerms(self, packet_id, data, seq):
        """ReqSubTerms european packet.

        ID: 62140100
        JP: 利用規約要求
        TR: Sub-terms of use request

        The game requests the sub-terms based on what it has already read.
        """
        version, unk, offset, size = struct.unpack(">IBII", data)
        assert version == TERMS_VERSION, "Terms and subterms version mismatch"
        self.sendAnsSubTerms(unk, offset, size, SUBTERMS[version], seq)

    def sendAnsSubTerms(self, unk, offset, size, subterms, seq):
        """AnsSubTerms european packet.

        ID: 62140200
        JP: サブ利用規約応答
        TR: Sub-terms of use response

        The server replies with the terms offset, size and chunk requested.
        """
        data = struct.pack(">BII", unk, offset, size)
        data += pati.lp2_string(subterms[offset:offset+size])
        self.send_packet(PatID4.AnsSubTerms, data, seq)

    def recvReqAnnounce(self, packet_id, data, seq):
        """ReqAnnounce packet.

        ID: 62300100
        JP: お知らせ要求
        TR: Notice request

        The game requests the announce text.
        """
        self.sendAnsAnnounce(ANNOUNCE, seq)

    def sendAnsAnnounce(self, announce, seq):
        """AnsAnnounce packet.

        ID: 62300200
        JP: お知らせ通知
        TR: Notice response

        The server replies with the announce text.
        """
        data = pati.lp2_string(announce)
        self.send_packet(PatID4.AnsAnnounce, data, seq)

    def recvReqNoCharge(self, packet_id, data, seq):
        """ReqNoCharge packet.

        ID: 62310100
        JP: 未課金メッセージ要求
        TR: Unpaid message request

        The game requests the no-charge text.

        NB:
         - Japanese servers were online paid.
         - Western servers were free-to-play.
        """
        self.sendAnsNoCharge(CHARGE, seq)

    def sendAnsNoCharge(self, no_charge, seq):
        """AnsNoCharge packet.

        ID: 62310200
        JP: 未課金メッセージ通知
        TR: Unpaid message response

        The server replies with the no-charge text.
        """
        data = pati.lp2_string(no_charge)
        self.send_packet(PatID4.AnsNoCharge, data, seq)

    def recvReqVulgarityInfoHighJAP(self, packet_id, data, seq):
        """ReqVulgarityInfoHigh japanese packet.

        ID: 62500100
        JP: 名前用禁止文言要求
        TR: Forbidden names request
        """
        self.sendAnsVulgarityInfoHighJAP(seq)

    def sendAnsVulgarityInfoHighJAP(self, seq):
        """AnsVulgarityInfoHigh japanese packet.

        ID: 62500200
        JP: 名前用禁止文言応答
        TR: Forbidden names response
        """
        unk = 1
        data = struct.pack(">II", unk, len(VULGARITY_INFO))
        self.send_packet(PatID4.AnsVulgarityInfoHighJAP, data, seq)

    def recvReqVulgarityInfoLowJAP(self, packet_id, data, seq):
        """ReqVulgarityInfoLow japanese packet.

        ID: 62520100
        JP: 名前以外用禁止文言要求
        TR: Forbidden words request
        """
        self.sendAnsVulgarityInfoLowJAP(seq)

    def sendAnsVulgarityInfoLowJAP(self, seq):
        """AnsVulgarityInfoLow japanese packet.

        ID: 62520200
        JP: 名前以外用禁止文言応答
        TR: Forbidden words response
        """
        unk = 1
        data = struct.pack(">II", unk, len(VULGARITY_INFO))
        self.send_packet(PatID4.AnsVulgarityInfoLowJAP, data, seq)

    def recvReqVulgarityInfoLow(self, packet_id, data, seq):
        """ReqVulgarityInfoLow packet.

        ID: 62560100
        JP: 真・名前以外用禁止文言要求
        TR: (New) Forbidden words request
        """
        info, = struct.unpack(">I", data)
        self.sendAnsVulgarityInfoLow(info, seq)

    def sendAnsVulgarityInfoLow(self, info, seq):
        """AnsVulgarityInfoLow packet.

        ID: 62560200
        JP: 真・名前以外用禁止文言応答
        TR: (New) Forbidden words response
        """
        unk = 1
        data = struct.pack(">III", unk, info, len(VULGARITY_INFO))
        self.send_packet(PatID4.AnsVulgarityInfoLow, data, seq)

    def recvReqVulgarityLow(self, packet_id, data, seq):
        """ReqVulgarityLow packet.

        ID: 62570100
        JP: 真・名前以外用禁止文言取得要求
        TR: (New) Get forbidden words request
        """
        unk, info, offset, size = struct.unpack(">IIII", data)
        self.sendAnsVulgarityLow(
            info, offset, size, VULGARITY_INFO, seq
        )

    def sendAnsVulgarityLow(self, info, offset, size, vulg, seq):
        """AnsVulgarityLow packet.

        ID: 62570200
        JP: 真・名前以外用禁止文言取得応答
        TR: (New) Get forbidden words response
        """
        data = struct.pack(">III", info, offset, size)
        data += pati.lp2_string(vulg)
        self.send_packet(PatID4.AnsVulgarityLow, data, seq)

    def recvReqCommonKey(self, packet_id, data, seq):
        """ReqCommonKey packet.

        ID: 60700100
        JP: 共通鍵要求
        TR: Common key request
        """
        self.sendAnsCommonKey(seq)

    def sendAnsCommonKey(self, seq):
        """AnsCommonKey packet.

        ID: 60700200
        JP: 共通鍵返答
        TR: Common key response

        TODO: Handle encryption properly.
        """
        # Bypass upcoming encryption by sending a dummy packet instead
        # self.send_packet(PatID4.AnsCommonKey, b'', seq)
        self.sendAnsAuthenticationToken(b'', seq)

    def recvReqLmpConnect(self, packet_id, data, seq):
        """ReqLmpConnect packet.

        ID: 62010100
        JP: LMPの接続先要求
        TR: LMP's access point request

        TODO: I don't think it's related to LMP protocol.
        """
        config = get_config("LMP")
        self.sendAnsLmpConnect(get_ip(config["IP"]), config["Port"], seq)

    def sendAnsLmpConnect(self, address, port, seq):
        """AnsLmpConnect packet.

        ID: 62010200
        JP: LMPの接続先応答
        TR: LMP's access point response

        TODO: Handle/Convert special addresses like 127.0.0.1 and 0.0.0.0.
        """
        data = struct.pack(">H", len(address))
        data += address.encode("ascii")
        data += struct.pack(">H", port)
        self.send_packet(PatID4.AnsLmpConnect, data, seq)

    def recvReqShut(self, packet_id, data, seq):
        """ReqShut packet.

        ID: 60100100
        JP: 切断要求
        TR: Disconnection request

        # 1: full logout(?)
        # 2: logout to different server(?)
        """
        shutdown_type, = struct.unpack(">B", data)
        self.sendAnsShut(shutdown_type, seq)

    def sendAnsShut(self, shutdown_type, seq):
        """AnsShut packet.

        ID: 60100200
        JP: 切断返答
        TR: Disconnection response
        """
        data = struct.pack(">B", shutdown_type)
        self.send_packet(PatID4.AnsShut, data, seq)
        if shutdown_type == 1:
            # Only modify request_reconnection if it's a 1 shutdown_type,
            # otherwise leave it at what it was before
            self.session.request_reconnection = False
        self.finish()

    def sendNtcShut(self, message, seq):
        """NtcShut packet.

        ID: 60101000
        JP: 切断返答
        TR: Disconnection notification
        """
        has_message = bool(message)
        data = struct.pack(">B", int(has_message))
        data += pati.lp2_string(message[:0x200])
        self.send_packet(PatID4.NtcShut, data, seq)

    def recvReqChargeInfo(self, packet_id, data, seq):
        """ReqChargeInfo packet.

        ID: 61020100
        JP: 課金情報要求
        TR: Billing information request
        """
        info_type, = struct.unpack('>B', data)
        self.sendAnsChargeInfo(info_type, seq)

    def sendAnsChargeInfo(self, info_type, seq):
        """AnsChargeInfo packet.

        ID: 61020200
        JP: 課金情報返答
        TR: Billing information response
        """
        info = pati.ChargeInfo()
        info.ticket_validity1 = pati.Long(
            int(timedelta(days=1).total_seconds())
        )
        info.ticket_validity2 = pati.Long(
            int(timedelta(days=1).total_seconds())
        )
        info.unk_binary_0x05 = pati.Binary("Cid")
        info.online_support_code = pati.String(self.session.get_support_code())
        data = info.pack()
        self.send_packet(PatID4.AnsChargeInfo, data, seq)

    def recvReqLoginInfo(self, packet_id, data, seq):
        """ReqLoginInfo packet.

        ID: 61010100
        JP: ログイン情報送信
        TR: Send login information
        """
        data = pati.LoginInfo.unpack(data)
        self.server.debug("LoginInfo: {!r}".format(data))
        self.sendAnsLoginInfo(seq)

    def sendAnsLoginInfo(self, seq):
        """AnsLoginInfo packet.

        ID: 61010200
        JP: ログイン情報返信
        TR: Login information response

        TODO: Implement this properly.
        """
        need_ticket = 1  # The game will call sendReqTicket if set to 1
        data = struct.pack(">B", need_ticket)
        data += pati.lp2_string("dummy_data")
        info = pati.ChargeInfo()
        info.online_support_code = pati.String(
            self.session.get_support_code())
        data += info.pack()
        self.send_packet(PatID4.AnsLoginInfo, data, seq)

    def recvReqTicket(self, packet_id, data, seq):
        """ReqTicket packet.

        ID: 60300100
        JP: ＰＡＴチケット要求
        TR: PAT ticket request

        It seems both the client and server can:
         - Send a PAT ticket
         - Receive a PAT ticket

        TODO: Investigate how PAT tickets should be used.
        """
        if packet_id == PatID4.ReqTicket:
            self.sendAnsTicket(seq)
        elif packet_id == PatID4.ReqTicket2:
            self.server.error("Unimplemented recvReqTicket")

    def sendAnsTicket(self, seq):
        """AnsTicket packet.

        ID: 60300200
        JP: ＰＡＴチケット返答
        TR: PAT ticket response
        """
        pat_ticket = self.session.new_pat_ticket()
        data = struct.pack(">H", len(pat_ticket)) + pat_ticket
        self.send_packet(PatID4.AnsTicket, data, seq)

    def recvReqUserListHead(self, packet_id, data, seq):
        """ReqUserListHead packet.

        ID: 61100100
        JP: PAT ID候補数要求
        TR: PAT ID candidate count request

        The games' instruction leaflets seem to refer "PAT ID" as "Capcom ID".
        """
        first_index, count = struct.unpack_from(">II", data)
        header = pati.unpack_bytes(data, 8)
        self.sendAnsUserListHead(first_index, count, header, seq)

    def sendAnsUserListHead(self, first_index, count, header, seq):
        """AnsUserListHead packet.

        ID: 61100200
        JP: PAT ID候補数応答
        TR: PAT ID candidate count response
        """
        data = struct.pack(">II", first_index, count)
        self.send_packet(PatID4.AnsUserListHead, data, seq)

    def recvReqUserListData(self, packet_id, data, seq):
        """ReqUserListData packet.

        ID: 61110100
        JP: PAT ID候補要求
        TR: PAT ID candidate request
        """
        first_index, count = struct.unpack(">II", data)
        self.sendAnsUserListData(first_index, count, seq)

    def sendAnsUserListData(self, first_index, count, seq):
        """AnsUserListData packet.

        ID: 61110200
        JP: PAT ID候補送信
        TR: Send PAT ID candidate

        TODO: Properly create/save/load Capcom ID profiles.
        """
        data = struct.pack(">II", first_index, count)
        for i, obj in self.session.get_users(first_index, count):
            capcom_id, info = obj
            user = pati.UserObject()
            user.slot_index = pati.Long(i)
            user.capcom_id = pati.String(capcom_id)
            if info.get("name"):
                user.hunter_name = pati.String(info["name"])
            data += user.pack()
        self.send_packet(PatID4.AnsUserListData, data, seq)

    def recvReqUserListFoot(self, packet_id, data, seq):
        """ReqUserList packet.

        ID: 61120100
        JP: PAT ID候補送信終了確認
        TR: PAT ID candidate end of transmission request
        """
        self.sendAnsUserListFoot(seq)

    def sendAnsUserListFoot(self, seq):
        """AnsUserListFoot packet.

        ID: 61120200
        JP: PAT ID候補送信終了返答
        TR: PAT ID candidate end of transmission response
        """
        self.send_packet(PatID4.AnsUserListFoot, b"", seq)

    def recvReqServerTime(self, packet_id, data, seq):
        """ReqServerTime packet.

        ID: 60020100
        JP: サーバ時刻要求
        TR: Server time request
        """
        converted_country_code, = struct.unpack(">I", data)
        self.sendAnsServerTime(converted_country_code, seq)

    def sendAnsServerTime(self, converted_country_code, seq):
        """AnsServerTime packet.

        ID: 60020200
        JP: サーバ時刻返答
        TR: Server time response
        """
        # Counter that ticks up once per second, Epoch works
        server_time = time_utils.current_server_time()
        # Always Epoch, used for Wii Shop subscription ticket
        current_time = time_utils.current_server_time()
        data = struct.pack(">II", server_time, current_time)
        self.send_packet(PatID4.AnsServerTime, data, seq)

    def recvReqUserObject(self, packet_id, data, seq):
        """ReqUserObject packet.

        ID: 61200100
        JP: ユーザオブジェクト送信
        TR: Send user object

        TODO: Find the purpose of all UserObject fields.
        """
        is_slot_empty, slot_index = struct.unpack_from(">BI", data)
        user_obj = pati.UserObject.unpack(data, 5)
        self.server.debug("UserObject: {}, {}, {!r}".format(
            is_slot_empty, slot_index, user_obj
        ))
        hunter_name = None
        if hasattr(user_obj, "hunter_name"):
            hunter_name = pati.unpack_string(user_obj.hunter_name)
        self.session.use_user(slot_index, hunter_name)
        user_obj.capcom_id = pati.String(self.session.capcom_id)
        self.server.info("Client {} Capcom ID `{}`".format(
            self.client_address, self.session.capcom_id
        ))
        self.sendAnsUserObject(is_slot_empty, slot_index, user_obj, seq)

    def sendAnsUserObject(self, is_slot_empty, slot_index, user_obj, seq):
        """AnsUserObject packet.

        ID: 61200200
        JP: ユーザオブジェクト結果
        TR: User object result

        TODO: Properly store/update user objects.
        """
        unused = 0
        need_ticket = 1
        data = struct.pack(">B", need_ticket)
        data += pati.lp2_string(b"Unk_UserObj_str")
        data += struct.pack(">I", unused)
        data += user_obj.pack()
        self.send_packet(PatID4.AnsUserObject, data, seq)

    def recvReqFmpListVersion(self, packet_id, data, seq):
        """ReqFmpListVersion packet.

        ID: 61300100 / 63100100
        JP: FMPリストバージョン確認
        TR: FMP list version check

        TODO:
         - Find why there are 2 versions of FMP packets.
         - Find why most of the 2 versions are ignored.
        """
        if packet_id == PatID4.ReqFmpListVersion:
            self.sendAnsFmpListVersion(seq)
        elif packet_id == PatID4.ReqFmpListVersion2:
            self.sendAnsFmpListVersion2(seq)

    def sendAnsFmpListVersion(self, seq):
        """AnsFmpListVersion packet.

        ID: 61300200
        JP: FMPリストバージョン確認応答
        TR: FMP list version acknowledgment
        """
        data = struct.pack(">I", FMP_VERSION)
        self.send_packet(PatID4.AnsFmpListVersion, data, seq)

    def sendAnsFmpListVersion2(self, seq):
        """AnsFmpListVersion2 packet.

        ID: 63100200
        JP: FMPリストバージョン確認応答
        TR: FMP list version acknowledgment
        """
        data = struct.pack(">I", FMP_VERSION)
        self.send_packet(PatID4.AnsFmpListVersion2, data, seq)

    def recvReqFmpListHead(self, packet_id, data, seq):
        """ReqFmpListHead packet.

        ID: 61310100 / 63110100
        JP: FMPリスト数送信 / FMPリスト数要求
        TR: Send FMP list count / FMP list count request
        """
        # TODO: Might be worth investigating these parameters as
        # they might be useful when using multiple FMP servers.
        version, first_index, count = struct.unpack_from(
            ">III", data
        )  # noqa: F841
        # TODO: Unpack it using pati.Unpacker
        header = pati.unpack_bytes(data, 12)  # noqa: F841
        if packet_id == PatID4.ReqFmpListHead:
            self.sendAnsFmpListHead(seq)
        elif packet_id == PatID4.ReqFmpListHead2:
            self.sendAnsFmpListHead2(seq)

    def sendAnsFmpListHead(self, seq):
        """AnsFmpListHead packet.

        ID: 61310200
        JP: FMPリスト数応答
        TR: FMP list count response
        """
        unused = 0
        count = len(self.session.get_servers())
        data = struct.pack(">II", unused, count)
        self.send_packet(PatID4.AnsFmpListHead, data, seq)

    def sendAnsFmpListHead2(self, seq):
        """AnsFmpListHead2 packet.

        ID: 63110200
        JP: FMPリスト数応答
        TR: FMP list count response

        TODO: Check if it's always ignored compared to the previous one.
        """
        unused = 0
        count = len(self.session.get_servers())
        data = struct.pack(">II", unused, count)
        self.send_packet(PatID4.AnsFmpListHead2, data, seq)

    def recvReqFmpListData(self, packet_id, data, seq):
        """ReqFmpListData packet.

        ID: 61320100 / 63120100
        JP: FMPリスト送信 / FMPリスト要求
        TR: Send FMP list / FMP list response
        """
        first_index, count = struct.unpack_from(">II", data)
        if packet_id == PatID4.ReqFmpListData:
            self.sendAnsFmpListData(first_index, count, seq)
        elif packet_id == PatID4.ReqFmpListData2:
            self.sendAnsFmpListData2(first_index, count, seq)

    def sendAnsFmpListData(self, first_index, count, seq):
        """AnsFmpListData packet.

        ID: 61320200
        JP: FMPリスト応答
        TR: FMP list response

        TODO:
         - Do more reverse engineering.
         - This packet seems to affect only the first entry.
        """
        unused = 0
        data = struct.pack(">II", unused, count)
        data += pati.get_fmp_servers(self.session, first_index, count)
        self.send_packet(PatID4.AnsFmpListData, data, seq)

    def sendAnsFmpListData2(self, first_index, count, seq):
        """AnsFmpListData2 packet.

        ID: 63120200
        JP: FMPリスト応答
        TR: FMP list response

        TODO:
         - Do more reverse engineering.
         - This packet seems to affect entries past the first one.
        """
        unused = 0
        data = struct.pack(">II", unused, count)
        data += pati.get_fmp_servers(self.session, first_index, count)
        self.send_packet(PatID4.AnsFmpListData2, data, seq)

    def recvReqFmpListFoot(self, packet_id, data, seq):
        """ReqFmpListFoot packet.

        ID: 61330100 / 63130100
        JP: FMPリスト送信終了 / FMPリスト終了送信
        TR: FMP list end of transmission / FMP list transmission end
        """
        if packet_id == PatID4.ReqFmpListFoot:
            self.sendAnsFmpListFoot(seq)
        elif packet_id == PatID4.ReqFmpListFoot2:
            self.sendAnsFmpListFoot2(seq)

    def sendAnsFmpListFoot(self, seq):
        """AnsFmpListFoot packet.

        ID: 61330200
        JP: FMPリスト送信終了
        TR: FMP list end of transmission
        """
        self.send_packet(PatID4.AnsFmpListFoot, b"", seq)

    def sendAnsFmpListFoot2(self, seq):
        """AnsFmpListFoot2 packet.

        ID: 63130200
        JP: FMPリスト終了返答
        TR: FMP list end of transmission response
        """
        self.send_packet(PatID4.AnsFmpListFoot2, b"", seq)

    def recvReqLayerEnd(self, packet_id, data, seq):
        """ReqLayerEnd packet.

        ID: 64020100
        JP: レイヤ終了要求
        TR: Layer end request
        """
        self.notify_layer_departure()
        self.sendAnsLayerEnd(seq)

    def sendAnsLayerEnd(self, seq):
        """AnsLayerEnd packet.

        ID: 64020200
        JP: レイヤ終了応答
        TR: Layer end response
        """
        self.session.layer_end()
        self.send_packet(PatID4.AnsLayerEnd, b"", seq)

    def recvReqFmpInfo(self, packet_id, data, seq):
        """ReqFmpInfo packet.

        ID: 61340100 / 63140100
        JP: FMPデータ要求 / FMPデータ要求
        TR: FMP data request

        TODO: Do not hardcode the data and find the meaning of all fields.
        """
        index, = struct.unpack_from(">I", data)
        fields = pati.unpack_bytes(data, 4)
        server = self.session.join_server(index)
        config = get_config("FMP")
        fmp_addr = get_ip(config["IP"])
        fmp_port = config["Port"]
        fmp_data = pati.FmpData()
        fmp_data.server_address = pati.String(server.addr or fmp_addr)
        fmp_data.server_port = pati.Word(server.port or fmp_port)
        fmp_data.assert_fields(fields)
        if packet_id == PatID4.ReqFmpInfo:
            self.sendAnsFmpInfo(fmp_data, fields, seq)
        elif packet_id == PatID4.ReqFmpInfo2:
            self.sendAnsFmpInfo2(fmp_data, fields, seq)

        # Preserve session in database, due to server selection
        self.session.request_reconnection = True

    def sendAnsFmpInfo(self, fmp_data, fields, seq):
        """AnsFmpInfo packet.

        ID: 61340200
        JP: FMPデータ返答
        TR: FMP data response
        """
        data = fmp_data.pack_fields(fields)
        self.send_packet(PatID4.AnsFmpInfo, data, seq)

    def sendAnsFmpInfo2(self, fmp_data, fields, seq):
        """AnsFmpInfo2 packet.

        ID: 63140200
        JP: FMPデータ返答
        TR: FMP data response
        """
        data = fmp_data.pack_fields(fields)
        self.send_packet(PatID4.AnsFmpInfo2, data, seq)

    def recvReqBinaryHead(self, packet_id, data, seq):
        """ReqBinaryHead packet.

        ID: 63020100
        JP: バイナリデータ開始要求
        TR: Binary data start request

        TODO: Find all binary types and their meaning.
        """
        binary_type, = struct.unpack(">B", data)
        self.sendAnsBinaryHead(binary_type, seq)

    def sendAnsBinaryHead(self, binary_type, seq):
        """AnsBinaryHead packet.

        ID: 63020200
        JP: バイナリデータ開始応答
        TR: Binary data start response

        Examples of types sent during the login process
         - English: 0x05, 0x01, 0x05, 0x02, 0x03, 0x04
         - Japanese: 0x0a, 0x01, 0x0a, 0x02, 0x03, 0x04
         - French: 0x14, 0x10, 0x14, 0x11, 0x12, 0x13
         - German: 0x23, 0x1f, 0x23, 0x20, 0x21, 0x22
         - Italian: 0x32, 0x2e, 0x32, 0x2f, 0x30, 0x31
         - Spanish: 0x41, 0x3d, 0x41, 0x3e, 0x3f, 0x40
        """
        binary = PAT_BINARIES[binary_type]
        content = binary["content"]
        if callable(content):
            content = content()
        data = struct.pack(">II", binary["version"], len(content))
        self.send_packet(PatID4.AnsBinaryHead, data, seq)

    def recvReqBinaryData(self, packet_id, data, seq):
        """ReqBinaryData packet.

        ID: 63030100
        JP: バイナリデータ要求
        TR: Binary data request

        TODO: Handle multiple versions of a binary
        """
        binary_type, version, offset, size = struct.unpack(">BIII", data)
        binary = PAT_BINARIES[binary_type]
        content = binary["content"]
        if callable(content):
            content = content()
        self.sendAnsBinaryData(version, offset, size, content, seq)

    def sendAnsBinaryData(self, version, offset, size, binary, seq):
        """AnsBinaryData packet.

        ID: 63030200
        JP: バイナリデータ応答
        TR: Binary data response
        """
        data = struct.pack(">III", version, offset, size)
        data += pati.lp2_string(binary[offset:offset+size])
        self.send_packet(PatID4.AnsBinaryData, data, seq)

    def recvReqBinaryFoot(self, packet_id, data, seq):
        """ReqBinaryFoot packet.

        ID: 63040100
        JP: バイナリデータ完了要求
        TR: Binary date end of transmission request
        """
        binary_type, = struct.unpack(">B", data)
        self.sendAnsBinaryFoot(binary_type, seq)

    def sendAnsBinaryFoot(self, binary_type, seq):
        """AnsBinaryData packet.

        ID: 63040200
        JP: バイナリデータ完了応答
        TR: Binary date end of transmission response
        """
        self.send_packet(PatID4.AnsBinaryFoot, b"", seq)

    def recvReqUserSearchHead(self, packet_id, data, seq):
        """ReqUserSearchHead packet.

        ID: 66330100
        JP: ユーザ検索数要求
        TR: User search count request

        Sent by the game when searching for players:
         - Online > Player Search > By Name
         - Online > Player Search > By Id
        """
        with pati.Unpacker(data) as unpacker:
            self.search_info = {
                "capcom_id": to_str(unpacker.lp2_string()),
                "hunter_name": unpacker.lp2_string(),
                "search": unpacker.detailed_optional_fields(),
                "offset": unpacker.struct(">I")[0],
                "limit": unpacker.struct(">I")[0],
                "fields": unpacker.bytes()
            }
        self.server.debug((
            "ReqUserSearchHead("
            "hunter_name={hunter_name!r}, capcom_id={capcom_id!r}, "
            "search={search!r}, offset={offset}, limit={limit}, "
            "fields={fields!r})"
        ).format(**self.search_info))
        self.sendAnsUserSearchHead(seq)

    def sendAnsUserSearchHead(self, seq):
        """AnsUserSearchHead packet.

        ID: 66330200
        JP: ユーザ検索数返答
        TR: User search count response
        """
        unk = 0
        self.search_data = self.session.find_users(
            self.search_info["capcom_id"], self.search_info["hunter_name"],
            self.search_info["offset"], self.search_info["limit"]
        )
        data = struct.pack(">II", unk, len(self.search_data))
        self.send_packet(PatID4.AnsUserSearchHead, data, seq)

    def recvReqUserSearchData(self, packet_id, data, seq):
        """ReqUserSearchData packet.

        ID: 66340100
        JP: ユーザ検索要求
        TR: User search request
        """
        offset, size = struct.unpack(">II", data)
        self.sendAnsUserSearchData(offset, size, seq)

    def sendAnsUserSearchData(self, offset, size, seq):
        """AnsUserSearchData packet.

        ID: 66340200
        JP: ユーザ検索返答
        TR: User search response
        """
        unk = 0
        users = self.search_data
        count = len(users)
        data = struct.pack(">II", unk, count)
        for user in users:
            user_info = pati.UserSearchInfo()
            user_info.capcom_id = pati.String(user.capcom_id)
            user_info.hunter_name = pati.String(user.hunter_name)
            user_info.stats = pati.Binary(user.hunter_info.pack())
            user_info.layer_host = pati.Binary(user.get_layer_host_data())
            user_info.assert_fields(self.search_info["fields"])
            data += user_info.pack()
            data += pati.pack_optional_fields(user.get_optional_fields())
        self.send_packet(PatID4.AnsUserSearchData, data, seq)

    def recvReqUserSearchFoot(self, packet_id, data, seq):
        """ReqUserSearchFoot packet.

        ID: 66350100
        JP: ユーザ検索終了要求
        TR: User search end of transmission request
        """
        self.sendAnsUserSearchFoot(seq)

    def sendAnsUserSearchFoot(self, seq):
        """AnsUserSearchFoot packet.

        ID: 66350200
        JP: ユーザ検索終了返答
        TR: User search end of transmission response
        """
        self.send_packet(PatID4.AnsUserSearchFoot, b"", seq)

    def recvReqUserSearchInfo(self, packet_id, data, seq):
        """ReqUserSearchInfo packet.

        ID: 66360100
        JP: ユーザ検索データ要求
        TR: User search data request
        """
        with pati.Unpacker(data) as unpacker:
            capcom_id = to_str(unpacker.lp2_string())
            search_info = unpacker.UserSearchInfo()
        self.server.debug("SearchInfo: {}, {!r}".format(capcom_id,
                                                        search_info))
        self.sendAnsUserSearchInfo(capcom_id, search_info, seq)

    def sendAnsUserSearchInfo(self, capcom_id, search_info, seq):
        """AnsUserSearchInfo packet.

        ID: 66360200
        JP: ユーザ検索データ返答
        TR: User search data response
        """
        user = self.session.find_user_by_capcom_id(capcom_id)
        if not user:
            # TODO: Find a better way to notify offline status in friend list
            user_info = pati.UserSearchInfo()
            user_info.capcom_id = pati.String(capcom_id)
            user_info.hunter_name = pati.String("OFFLINE")
            data = user_info.pack() + pati.pack_optional_fields([])
            self.sendAnsAlert(PatID4.AnsUserSearchInfo, data, seq)
            return

        user_info = pati.UserSearchInfo()
        user_info.capcom_id = pati.String(user.capcom_id)
        user_info.hunter_name = pati.String(user.hunter_name)
        user_info.stats = pati.Binary(user.hunter_info.pack())
        user_info.layer_host = pati.Binary(user.get_layer_host_data())

        user_info.unk_byte_0x07 = pati.Byte(1)
        user_info.server_name = pati.String("\t".join([
            user.local_info["server_name"] or "",
            user.local_info["gate_name"] or "",
            user.local_info["city_name"] or ""
        ]))
        user_info.unk_byte_0x0b = pati.Byte(1)
        user_info.unk_string_0x0c = pati.String("StrC")
        user_info.city_capacity = pati.Long(4)
        user_info.city_size = pati.Long(3)

        # This fields are used to identify a user.
        # Specifically when a client is deserializing data from the packets
        # `NtcLayerBinary` and `NtcLayerBinary2`
        # TODO: Proper field value and name
        user_info.info_mine_0x0f = pati.Long(int(hash(user.capcom_id))
                                             & 0xffffffff)
        user_info.info_mine_0x10 = pati.Long(int(hash(user.capcom_id[::-1]))
                                             & 0xffffffff)

        data = user_info.pack()
        # TODO: Figure out the optional fields
        data += pati.pack_optional_fields([])
        self.send_packet(PatID4.AnsUserSearchInfo, data, seq)

    def recvReqLayerStart(self, packet_id, data, seq):
        """ReqLayerStart packet.

        ID: 64010100
        JP: レイヤ開始要求
        TR: Layer start request
        """
        unk1 = pati.unpack_bytes(data)
        unk2 = pati.unpack_bytes(data, len(unk1) + 1)
        self.sendAnsLayerStart(unk1, unk2, seq)

    def sendAnsLayerStart(self, unk1, unk2, seq):
        """AnsLayerStart packet.

        ID: 64010200
        JP: レイヤ開始応答
        TR: Layer start response
        """
        layer = self.session.layer_start()
        self.send_packet(PatID4.AnsLayerStart, layer.pack(), seq)

    def sendNtcCircleLeave(self, circle, circle_index, seq):
        """NtcCircleLeave packet.

        ID: 65041000
        JP: サークルアウト通知
        TR: Circle out notification
        """

        player_index = circle.players.index(self.session) + 1
        data = struct.pack(">I", circle_index)
        data += pati.lp2_string(self.session.capcom_id)
        data += struct.pack(">B", player_index)

        unk01 = 0x00  # Flag of some sort
        data += struct.pack(">B", unk01)

        self.server.circle_broadcast(circle, PatID4.NtcCircleLeave, data, seq,
                                     self.session)

    def recvReqCircleInfoNoticeSet(self, packet_id, data, seq):
        """ReqCircleInfoNoticeSet packet.

        ID: 65800100
        JP: サークル通知定義登録要求
        TR: Circle notification subscription request
        """
        unk1 = pati.unpack_bytes(data)
        unk2 = pati.unpack_bytes(data, len(unk1) + 1)
        self.sendAnsCircleInfoNoticeSet(unk1, unk2, seq)

    def sendAnsCircleInfoNoticeSet(self, unk1, unk2, seq):
        """AnsCircleInfoNoticeSet packet.

        ID: 65800200
        JP: サークル通知定義登録返答
        TR: Circle notification subscription response
        """
        self.send_packet(PatID4.AnsCircleInfoNoticeSet, b"", seq)

    def recvNtcCheatCheck(self, packet_id, data, seq):
        """NtcCheatCheck packet.

        ID: 60801000
        JP: チートチェックデータ送信
        TR: Send cheat check data

        TODO: Handle cheat check data.
        """
        pass

    def recvReqUserSearchSet(self, packet_id, data, seq):
        """ReqUserSearchSet packet.

        ID: 66300100
        JP: ユーザ検索設定要求
        TR: User search settings request
        """
        extra = pati.unpack_optional_fields(data)
        self.server.debug("UserSearchSet: {!r}".format(extra))
        self.sendAnsUserSearchSet(extra, seq)

    def sendAnsUserSearchSet(self, extra, seq):
        """AnsUserSearchSet packet.

        ID: 66300200
        JP: ユーザ検索設定返答
        TR: User search settings response
        """
        self.send_packet(PatID4.AnsUserSearchSet, b"", seq)

    def recvReqBinaryVersion(self, packet_id, data, seq):
        """ReqBinaryVersion packet.

        ID: 63010100
        JP: バイナリバージョン確認
        TR: Binary version check
        """
        unk, = struct.unpack(">B", data)
        self.sendAnsBinaryVersion(unk, seq)

    def sendAnsBinaryVersion(self, unk, seq):
        """AnsBinaryVersion packet.

        ID: 63010200
        JP: バイナリバージョン確認応答
        TR: Binary version acknowledgment
        """
        unused = 0
        version = 1  # The game might send binary requests for this version
        data = struct.pack(">BI", unused, version)
        self.send_packet(PatID4.AnsBinaryVersion, data, seq)

    def recvReqLayerUserListHead(self, packet_id, data, seq):
        """ReqLayerUserListHead packet.

        ID: 64640100
        JP: レイヤユーザリスト数要求
        TR: Layer user list count request
        """
        with pati.Unpacker(data) as unpacker:
            unk, = unpacker.struct(">B")
            layer = unpacker.lp2_string()
            first_index, count = unpacker.struct(">II")
            fields = unpacker.bytes()
        self.server.debug("LayerUserListHead({}, {!r}, {}, {}, {!r}".format(
                          unk, layer, first_index, count, fields))
        self.sendAnsLayerUserListHead(unk, layer, first_index, count, fields,
                                      seq)

    def sendAnsLayerUserListHead(self, unk, layer, first_index, count,
                                 fields,
                                 seq):
        """AnsLayerUserListHead packet.

        ID: 64640200
        JP: レイヤユーザリスト数返答
        TR: Layer user list count response
        """
        depth, server_id, unk_id, gate_id, city_id = struct.unpack_from(
            ">IIHHH", layer)
        self.search_data = self.session.find_users_by_layer(
            server_id, gate_id, city_id, first_index, count)
        data = struct.pack(">II", first_index, len(self.search_data))
        self.send_packet(PatID4.AnsLayerUserListHead, data, seq)

    def recvReqLayerUserListData(self, packet_id, data, seq):
        """ReqLayerUserListData packet.

        ID: 64650100
        JP: レイヤユーザリスト要求
        TR: Layer user list request
        """
        first_index, count = struct.unpack(">II", data)
        self.sendAnsLayerUserListData(first_index, count, seq)

    def sendAnsLayerUserListData(self, first_index, count, seq):
        """AnsLayerUserListData packet.

        ID: 64650200
        JP: レイヤユーザリスト返答
        TR: Layer user list response
        """
        unk = 1
        users = self.search_data
        data = struct.pack(">II", unk, len(users))
        for _, user in users:
            layer_user = pati.LayerUserInfo()
            layer_user.capcom_id = pati.String(user.capcom_id)
            layer_user.hunter_name = pati.String(user.hunter_name)
            layer_user.layer_host = pati.Binary(user.get_layer_host_data())
            data += layer_user.pack()
            data += pati.pack_optional_fields(user.get_optional_fields())
        self.send_packet(PatID4.AnsLayerUserListData, data, seq)

    def recvReqLayerUserListFoot(self, packet_id, data, seq):
        """ReqLayerUserListFoot packet.

        ID: 64660100
        JP: レイヤユーザリスト終了要求
        TR: Layer user list end of transmission request
        """
        self.sendAnsLayerUserListFoot(seq)

    def sendAnsLayerUserListFoot(self, seq):
        """AnsLayerUserListFoot packet.

        ID: 64660200
        JP: レイヤユーザリスト終了返答
        TR: Layer user list end of transmission response
        """
        data = b""
        self.send_packet(PatID4.AnsLayerUserListFoot, data, seq)

    def recvReqLayerUserSearchHead(self, packet_id, data, seq):
        """ReqLayerUserSearchHead packet.

        ID: 64670100
        JP: レイヤユーザ検索リスト数要求
        TR: Layer user search list count request

        Sent by the game when searching for players at the gate:
         - Online > Player Search > Gate Search
        """
        with pati.Unpacker(data) as unpacker:
            self.search_info = {
                "unk": unpacker.struct(">B")[0],
                "layer": unpacker.lp2_string(),
                "capcom_id": to_str(unpacker.lp2_string()),
                "hunter_name": unpacker.lp2_string(),
                "search": unpacker.detailed_optional_fields(),
                "offset": unpacker.struct(">I")[0],
                "limit": unpacker.struct(">I")[0],
                "fields": unpacker.bytes()
            }
        self.server.debug((
            "ReqLayerUserSearchHead("
            "unk={unk}, layer={layer!r}, "
            "capcom_id={capcom_id!r}, hunter_name={hunter_name!r}, "
            "search={search!r}, offset={offset}, limit={limit}, "
            "fields={fields!r})"
        ).format(**self.search_info))
        self.sendAnsLayerUserSearchHead(seq)

    def sendAnsLayerUserSearchHead(self, seq):
        """AnsLayerUserSearchHead packet.

        ID: 64670200
        JP: レイヤユーザ検索リスト数返答
        TR: Layer user search list count response
        """
        depth, server_id, unk_id, gate_id, city_id = struct.unpack_from(
            ">IIHHH", self.search_info["layer"]
        )
        self.search_data = self.session.find_users_by_layer(
            server_id, gate_id, city_id,
            self.search_info["offset"], self.search_info["limit"],
            recursive=True
        )
        unk = 0
        data = struct.pack(">II", unk, len(self.search_data))
        self.send_packet(PatID4.AnsLayerUserSearchHead, data, seq)

    def recvReqLayerUserSearchData(self, packet_id, data, seq):
        """ReqLayerUserSearchData packet.

        ID: 64680100
        JP: レイヤユーザ検索リスト要求
        TR: Layer user search list request
        """
        offset, size = struct.unpack(">II", data)
        self.sendAnsLayerUserSearchData(offset, size, seq)

    def sendAnsLayerUserSearchData(self, offset, size, seq):
        """AnsLayerUserSearchData packet.

        ID: 64680200
        JP: レイヤユーザ検索リスト返答
        TR: Layer user search list response
        """
        unk = 0
        layer_users = self.search_data
        count = len(layer_users)
        data = struct.pack(">II", unk, count)
        for _, user in layer_users:
            layer_user = pati.LayerUserInfo()
            layer_user.capcom_id = pati.String(user.capcom_id)
            layer_user.hunter_name = pati.String(user.hunter_name)
            layer_user.layer_host = pati.Binary(user.get_layer_host_data())
            layer_user.assert_fields(self.search_info["fields"])
            data += layer_user.pack()
            data += pati.pack_optional_fields(user.get_optional_fields())
        self.send_packet(PatID4.AnsLayerUserSearchData, data, seq)

    def recvReqLayerUserSearchFoot(self, packet_id, data, seq):
        """ReqLayerUserSearchFoot packet.

        ID: 64690100
        JP: レイヤユーザ検索リスト終了要求
        TR: Layer user search list end of transmission request
        """
        self.sendAnsLayerUserSearchFoot(seq)

    def sendAnsLayerUserSearchFoot(self, seq):
        """AnsLayerUserSearchFoot packet.

        ID: 64690200
        JP: レイヤユーザ検索リスト終了返答
        TR: Layer user search list end of transmission response
        """
        self.send_packet(PatID4.AnsLayerUserSearchFoot, b"", seq)

    def recvReqFriendList(self, packet_id, data, seq):
        """ReqFriendList packet.

        ID: 66540100
        JP: フレンドリスト要求
        TR: Friend list request
        """
        with pati.Unpacker(data) as unpacker:
            first_index, count = unpacker.struct(">II")
            fields = unpacker.bytes()
        self.sendAnsFriendList(first_index, count, fields, seq)

    def sendAnsFriendList(self, first_index, count, fields, seq):
        """AnsFriendList packet.

        ID: 66540200
        JP: フレンドリスト返答
        TR: Friend list response
        """
        unk = 0
        friends = self.session.get_friends(first_index, count)
        count = len(friends)
        data = struct.pack(">II", unk, count)
        for index, (capcom_id, hunter_name) in enumerate(friends, 1):
            friend = pati.FriendData()
            friend.index = pati.Long(index)
            friend.capcom_id = pati.String(capcom_id)
            friend.hunter_name = pati.String(hunter_name)
            friend.assert_fields(fields)
            data += friend.pack()
        self.send_packet(PatID4.AnsFriendList, data, seq)

    def recvReqBlackAdd(self, packet_id, data, seq):
        """ReqBlackAdd packet.

        ID: 66600100
        JP: ブラックデータ登録要求
        TR: Black data registration request

        TODO: Implement it properly
        """
        with pati.Unpacker(data) as unpacker:
            capcom_id = to_str(unpacker.lp2_string())
            black_data = unpacker.BlackListUserData()
        self.sendAnsBlackAdd(capcom_id, black_data, seq)

    def sendAnsBlackAdd(self, capcom_id, black_data, seq):
        """AnsBlackAdd packet.

        ID: 66600200
        JP: ブラックデータ登録返答
        TR: Black data registration response
        """
        self.send_packet(PatID4.AnsBlackAdd, b"", seq)

    def recvReqBlackDelete(self, packet_id, data, seq):
        """ReqBlackDelete packet.

        ID: 66610100
        JP: ブラックデータ削除要求
        TR: Black data deletion request
        """
        capcom_id = to_str(pati.unpack_lp2_string(data))
        self.sendAnsBlackDelete(capcom_id, seq)

    def sendAnsBlackDelete(self, capcom_id, seq):
        """AnsBlackDelete packet.

        ID: 66610200
        JP: ブラックデータ削除返答
        TR: Black data deletion response
        """
        self.send_packet(PatID4.AnsBlackDelete, b"", seq)

    def recvReqBlackList(self, packet_id, data, seq):
        """ReqBlackList packet.

        ID: 66620100
        JP: ブラックリスト要求
        TR: Blacklist request

        TODO: Implement it properly
        """
        unk1, unk2 = struct.unpack_from(">II", data)  # 1st/last index?
        unk3 = data[8:]  # PAT fields filter? (1,2,3)?
        self.sendAnsBlackList(unk1, unk2, unk3, seq)

    def sendAnsBlackList(self, unk1, unk2, unk3, seq):
        """AnsBlackList packet.

        ID: 66620200
        JP: ブラックリスト返答
        TR: Blacklist response
        """
        dummy = pati.BlackListUserData()
        dummy.index = pati.Long(0)
        dummy.capcom_id = pati.String("")
        dummy.hunter_name = pati.String("")
        blacklisted_users = [dummy]
        unk = 0
        count = len(blacklisted_users)
        data = struct.pack(">II", unk, count)
        data += b"".join([item.pack() for item in blacklisted_users])
        self.send_packet(PatID4.AnsBlackList, data, seq)

    def recvNtcLayerChat(self, packet_id, data, seq):
        """NtcLayerChat packet.

        ID: 64721000
        JP: レイヤチャット通知
        TR: Layer chat notification

        The game sends a chat message to relay.

        NB: The message won't be displayed if the Capcom ID is blank.
        """
        with pati.Unpacker(data) as unpacker:
            unk1, = unpacker.struct(">B")
            info = unpacker.MessageInfo()
            message = unpacker.lp2_string()
        self.server.debug("NtcLayerChat: {}, {!r}, {}".format(
            unk1, info, message))
        self.sendNtcLayerChat(unk1, info, message, seq)

    def sendNtcLayerChat(self, unk1, info, message, seq):
        """NtcLayerChat packet.

        ID: 64721000
        JP: レイヤチャット送信
        TR: Layer chat transmission
        NB: Request and response share the same packet ID

        The server sends a chat message.
        """
        data = struct.pack(">B", unk1)

        info.text_color = pati.Long(LAYER_CHAT_COLORS[self.session.layer])
        info.sender_id = pati.String(self.session.capcom_id)
        info.sender_name = pati.String(self.session.hunter_name)

        data += info.pack()
        data += pati.lp2_string(message)

        self.server.layer_broadcast(self.session, PatID4.NtcLayerChat, data,
                                    seq)

    def recvReqLayerTell(self, packet_id, data, seq):
        """ReqLayerTell packet.

        ID: 64730100
        JP: レイヤ相手指定チャット送信
        TR: Layer specified chat transmission
        """
        with pati.Unpacker(data) as unpacker:
            recipient_id = to_str(unpacker.lp2_string())
            info = unpacker.MessageInfo()
            message = unpacker.lp2_string()
        self.server.debug("ReqTell: {}, {!r}, {}".format(
            recipient_id, info, message))
        self.sendAnsLayerTell(recipient_id, info, message, seq)

    def sendAnsLayerTell(self, recipient_id, info, message, seq):
        """AnsLayerTell packet.

        ID: 64730200
        JP: レイヤ相手指定チャット返信
        TR: Layer partner specified chat reply
        """
        self.send_packet(PatID4.AnsLayerTell, b"", seq)
        self.sendNtcLayerTell(recipient_id, info, message, seq)

    def sendNtcLayerTell(self, recipient_id, info, message, seq):
        """NtcLayerTell packet.

        ID: 64731000
        JP: レイヤ相手指定チャット通知
        TR: Layer partner specified chat notification
        """
        data = pati.lp2_string(recipient_id)
        info.unk_long_0x02 = pati.Long(20)
        info.sender_id = pati.String(self.session.capcom_id)
        info.sender_name = pati.String(self.session.hunter_name)
        data += info.pack()
        data += pati.lp2_string(message)
        self.send_packet(PatID4.NtcLayerTell, data, seq)
        for _, player in self.session.get_layer_players():
            if player.capcom_id == recipient_id:
                handler = self.server.get_pat_handler(player)
                if handler:
                    handler.try_send_packet(PatID4.NtcLayerTell, data, seq)

    def recvNtcCircleChat(self, packet_id, data, seq):
        """NtcCircleChat packet.

        ID: 65721000
        JP: サークルチャット通知
        TR: Circle chat notification
        """
        with pati.Unpacker(data) as unpacker:
            info = unpacker.MessageInfo()
            message = unpacker.lp2_string()
        self.server.debug("NtcCircleChat: {!r}, {}".format(
            info, message))
        self.sendNtcCircleChat(info, message, seq)

    def sendNtcCircleChat(self, info, message, seq):
        """NtcCircleChat packet.

        ID: 65721000
        JP: サークルチャット送信
        TR: Circle chat transmission
        """
        info.sender_id = pati.String(self.session.capcom_id)
        info.sender_name = pati.String(self.session.hunter_name)

        data = info.pack()
        data += pati.lp2_string(message)

        circle = self.session.get_circle()
        self.server.circle_broadcast(circle, PatID4.NtcCircleChat, data,
                                     seq, self.session)

    def recvReqTell(self, packet_id, data, seq):
        """ReqTell packet.

        ID: 66110100
        JP: 相手指定チャット送信
        TR: Send partner message
        """
        with pati.Unpacker(data) as unpacker:
            recipient_id = to_str(unpacker.lp2_string())
            info = unpacker.MessageInfo()
            message = unpacker.lp2_string()
        self.server.debug("ReqTell: {}, {!r}, {}".format(
            recipient_id, info, message))
        self.sendAnsTell(recipient_id, info, message, seq)

    def sendAnsTell(self, recipient_id, info, message, seq):
        """AnsTell packet.

        ID: 66110200
        JP: 相手指定チャット返信
        TR: Receive partner message
        """
        self.send_packet(PatID4.AnsTell, b"", seq)
        self.sendNtcTell(recipient_id, info, message, seq)

    def sendNtcTell(self, recipient_id, info, message, seq):
        """NtcTell packet.

        ID: 66111000
        JP: 相手指定チャット通知
        TR: Partner message notification
        """
        data = b""
        data += pati.lp2_string(recipient_id)
        info.unk_long_0x02 = pati.Long(20)
        info.sender_id = pati.String(self.session.capcom_id)
        info.sender_name = pati.String(self.session.hunter_name)
        data += info.pack()
        data += pati.lp2_string(message)
        self.try_send_packet_to(recipient_id, PatID4.NtcTell, data, seq)

    def recvReqFriendAdd(self, packet_id, data, seq):
        """ReqFriendAdd packet.

        ID: 66500100
        JP: フレンド登録要求
        TR: Friend registration request

        TODO: Merge this with ReqTell?
        """
        with pati.Unpacker(data) as unpacker:
            recipient_id = to_str(unpacker.lp2_string())
            info = unpacker.MessageInfo()
            message = unpacker.lp2_string()
        self.server.debug("ReqFriendAdd: {}, {!r}, {}".format(
            recipient_id, info, message))
        self.sendAnsFriendAdd(recipient_id, info, message, seq)

    def sendAnsFriendAdd(self, recipient_id, info, message, seq):
        """AnsFriendAdd packet.

        ID: 66500200
        JP: フレンド登録返答
        TR: Friend registration response
        """
        if not self.session.add_friend_request(recipient_id):
            self.sendAnsAlert(PatID4.AnsFriendAdd,
                              "<LF=8><BODY><CENTER>Unknown Capcom ID.<END>",
                              seq)
            return
        self.send_packet(PatID4.AnsFriendAdd, b"", seq)
        self.sendNtcFriendAccept(recipient_id, info, message, seq)

    def sendNtcFriendAdd(self, recipient_id, accepted, seq):
        """NtcFriendAdd packet.

        ID: 66501000
        JP: フレンド登録完了通知
        TR: Friend registration completed notification
        """
        if not accepted:
            return

        # Send notification to friend
        data = b""
        data += pati.lp2_string(recipient_id)
        friend = pati.FriendData()
        friend.index = pati.Long(1)  # TODO: Reverse-engineer this field
        friend.capcom_id = pati.String(self.session.capcom_id)
        friend.hunter_name = pati.String(self.session.hunter_name)
        data += friend.pack()
        data += struct.pack(">B", accepted)
        self.try_send_packet_to(recipient_id, PatID4.NtcFriendAdd, data, seq)

        # Send notification to self
        data = pati.lp2_string(self.session.capcom_id)
        friend = pati.FriendData()
        friend.index = pati.Long(1)   # TODO: Reverse-engineer this field
        friend.capcom_id = pati.String(recipient_id)
        friend.hunter_name = pati.String(
            self.session.get_user_name(recipient_id))
        data += friend.pack()
        data += struct.pack(">B", accepted)
        self.send_packet(PatID4.NtcFriendAdd, data, seq)

    def recvReqFriendAccept(self, packet_id, data, seq):
        """ReqFriendAccept packet.

        ID: 66510100
        JP: フレンド登録依頼返答要求
        TR: Friend registration accept request
        """
        with pati.Unpacker(data) as unpacker:
            recipient_id = to_str(unpacker.lp2_string())
            accepted, = unpacker.struct(">B")
        self.sendAnsFriendAccept(recipient_id, accepted, seq)
        self.sendNtcFriendAdd(recipient_id, accepted, seq)

    def sendAnsFriendAccept(self, recipient_id, accepted, seq):
        """AnsFriendAccept packet.

        ID: 66510200
        JP: フレンド登録依頼返答返答
        TR: Friend registration accept response
        """
        self.session.accept_friend(recipient_id, accepted)
        self.send_packet(PatID4.AnsFriendAccept, b"", seq)

    def sendNtcFriendAccept(self, recipient_id, info, message, seq):
        """NtcFriendAccept packet.

        ID: 66511000
        JP: フレンド登録依頼通知
        TR: Friend registration request notification

        TODO: Merge this with NtcTell?
        """
        data = b""
        data += pati.lp2_string(recipient_id)
        info.unk_long_0x02 = pati.Long(20)
        info.sender_id = pati.String(self.session.capcom_id)
        info.sender_name = pati.String(self.session.hunter_name)
        data += info.pack()
        data += pati.lp2_string(message)
        self.try_send_packet_to(recipient_id, PatID4.NtcFriendAccept, data,
                                seq)

    def recvReqFriendDelete(self, packet_id, data, seq):
        """ReqFriendDelete packet.

        ID: 66530100
        JP: フレンドデータ削除要求
        TR: Friend data deletion request
        """
        capcom_id = to_str(pati.unpack_lp2_string(data))
        self.sendAnsFriendDelete(capcom_id, seq)

    def sendAnsFriendDelete(self, capcom_id, seq):
        """AnsFriendDelete packet.

        ID: 66530200
        JP: フレンドデータ削除返答
        TR: Friend data deletion response
        """
        self.session.delete_friend(capcom_id)
        self.send_packet(PatID4.AnsFriendDelete, b"", seq)

    def recvReqLayerChildListHead(self, packet_id, data, seq):
        """ReqLayerChildListHead packet.

        ID: 64240100
        JP: 子レイヤリスト数要求
        TR: Child layer list count request
        """
        unk1, unk2 = struct.unpack_from(">II", data)  # 1st/last index?
        layer_info = data[8:8+0xf]
        self.sendAnsLayerChildListHead(unk1, unk2, layer_info, seq)

    def sendAnsLayerChildListHead(self, unk1, unk2, layer_info, seq):
        """AnsLayerChildListHead packet.

        ID: 64240200
        JP: 子レイヤリスト数返答
        TR: Child layer list count response
        """
        unk = 0
        count = len(self.session.get_layer_children())
        data = struct.pack(">II", unk, count)
        self.send_packet(PatID4.AnsLayerChildListHead, data, seq)

    def recvReqLayerChildListData(self, packet_id, data, seq):
        """ReqLayerChildListData packet.

        ID: 64250100
        JP: 子レイヤリスト要求
        TR: Child layer list request
        """
        first_index, count = struct.unpack_from(">II", data)
        self.sendAnsLayerChildListData(first_index, count, seq)

    def sendAnsLayerChildListData(self, first_index, count, seq):
        """AnsLayerChildListData packet.

        ID: 64250200
        JP: 子レイヤリスト返答
        TR: Child layer list response
        """
        unk = first_index
        data = struct.pack(">II", unk, count)
        data += pati.get_layer_children(self.session, first_index, count)
        self.send_packet(PatID4.AnsLayerChildListData, data, seq)

    def recvReqLayerChildListFoot(self, packet_id, data, seq):
        """ReqLayerChildListFoot packet.

        ID: 64260100
        JP: 子レイヤリスト終了要求
        TR: Child layer list end of transmission request
        """
        self.sendAnsLayerChildListFoot(seq)

    def sendAnsLayerChildListFoot(self, seq):
        """AnsLayerChildListFoot packet.

        ID: 64260200
        JP: 子レイヤリスト終了返答
        TR: Child layer list end of transmission response
        """
        self.send_packet(PatID4.AnsLayerChildListFoot, b"", seq)

    def recvReqLayerSiblingListHead(self, packet_id, data, seq):
        """ReqLayerSiblingListHead packet.

        ID: 64270100
        JP: 兄弟レイヤリスト数要求
        TR: Layer sibling list count request

        Sent by the game when leaving the gate via the entrance:
         - Relocate > Change Gates

        TODO: Merge this with ReqLayerChildListHead?
        """
        unk1, unk2 = struct.unpack_from(">II", data)  # 1st/last index?
        layer_info = data[8:8+0xf]
        self.sendAnsLayerSiblingListHead(unk1, unk2, layer_info, seq)

    def sendAnsLayerSiblingListHead(self, unk1, unk2, layer_info, seq):
        """AnsLayerSiblingListHead packet.

        ID: 64270200
        JP: 兄弟レイヤリスト数返答
        TR: Layer sibling list count response

        TODO: Merge this with AnsLayerChildListHead?
        """
        unk = 0
        count = len(self.session.get_layer_sibling())
        data = struct.pack(">II", unk, count)
        self.send_packet(PatID4.AnsLayerSiblingListHead, data, seq)

    def recvReqLayerSiblingListData(self, packet_id, data, seq):
        """ReqLayerSiblingListData packet.

        ID: 64280100
        JP: 兄弟レイヤリスト要求
        TR: Layer sibling list request

        TODO: Merge this with ReqLayerChildListData?
        """
        first_index, count = struct.unpack_from(">II", data)
        self.sendAnsLayerSiblingListData(first_index, count, seq)

    def sendAnsLayerSiblingListData(self, first_index, count, seq):
        """AnsLayerSiblingListData packet.

        ID: 64280200
        JP: 兄弟レイヤリスト返答
        TR: Layer sibling list response

        TODO: Merge this with AnsLayerChildListData?
        """
        unk = first_index
        data = struct.pack(">II", unk, count)
        data += pati.get_layer_sibling(self.session, first_index, count)
        self.send_packet(PatID4.AnsLayerSiblingListData, data, seq)

    def recvReqLayerSiblingListFoot(self, packet_id, data, seq):
        """ReqLayerSiblingListFoot packet.

        ID: 64290100
        JP: 兄弟レイヤリスト終了要求
        TR: Layer sibling list end of transmission request
        """
        self.sendAnsLayerSiblingListFoot(seq)

    def sendAnsLayerSiblingListFoot(self, seq):
        """AnsLayerSiblingListFoot packet.

        ID: 64290200
        JP: 兄弟レイヤリスト終了返答
        TR: Layer sibling list end of transmission response
        """
        self.send_packet(PatID4.AnsLayerSiblingListFoot, b"", seq)

    def recvReqLayerChildInfo(self, packet_id, data, seq):
        """ReqLayerChildInfo packet.

        ID: 64230100
        JP: 子レイヤ情報要求
        TR: Child layer information request
        """
        unk1, = struct.unpack_from(">H", data)
        layer_data = data[2:]  # layer_data with some unknown ones appended
        self.sendAnsLayerChildInfo(unk1, layer_data, seq)

    def sendAnsLayerChildInfo(self, unk1, layer_data, seq):
        """AnsLayerChildInfo packet.

        ID: 64230200
        JP: 子レイヤ情報返答
        TR: Child layer information response
        """
        data = struct.pack(">H", 1)
        data += pati.getDummyLayerData().pack()
        data += b"\0" * 2
        self.send_packet(PatID4.AnsLayerChildInfo, data, seq)

    def recvReqLayerDown(self, packet_id, data, seq):
        """ReqLayerDown packet.

        ID: 64140100
        JP: レイヤダウン要求（番号指定）
        TR: Layer down request (number specified)
        """
        layer_id, = struct.unpack_from(">H", data)  # WordInc
        layer_set = data[2:]  # TODO parse LayerSet
        self.sendAnsLayerDown(layer_id, layer_set, seq)

    def sendAnsLayerDown(self, layer_id, layer_set, seq):
        """AnsLayerDown packet.

        ID: 64140200
        JP: レイヤダウン返答
        TR: Layer down response
        """
        data = struct.pack(">H", layer_id)
        self.session.layer_down(layer_id)
        self.send_packet(PatID4.AnsLayerDown, data, seq)

    def recvReqUserStatusSet(self, packet_id, data, seq):
        """ReqUserStatusSet packet.

        ID: 66400100
        JP: ユーザステータス設定要求
        TR: User status settings request
        """
        status_set = pati.UserStatusSet.unpack(data)
        self.server.debug("UserStatusSet: {!r}".format(status_set))
        self.sendAnsUserStatusSet(status_set, seq)

    def sendAnsUserStatusSet(self, status_set, seq):
        """AnsUserStatusSet packet.

        ID: 66400200
        JP: ユーザステータス設定返答
        TR: User status settings response
        """
        self.send_packet(PatID4.AnsUserStatusSet, b"", seq)

    def recvReqUserBinaryNotice(self, packet_id, data, seq):
        """ReqUserBinaryNotice packet.

        ID: 66320100
        JP: ユーザ表示用バイナリ通知要求
        TR: User display binary notification request
        """
        with pati.Unpacker(data) as unpacker:
            unk1, = unpacker.struct(">B")
            capcom_id = to_str(unpacker.lp2_string())
            offset, length = unpacker.struct(">II")
        self.sendAnsUserBinaryNotice(unk1, capcom_id, offset, length, seq)

    def sendAnsUserBinaryNotice(self, unk1, capcom_id, offset, length, seq):
        """AnsUserBinaryNotice packet.

        ID: 66320200
        JP: ユーザ表示用バイナリ通知返答
        TR: User display binary notification response
        """
        self.sendNtcUserBinaryNotice(unk1, capcom_id, offset, length, seq)
        self.send_packet(PatID4.AnsUserBinaryNotice, b"", seq)

    def sendNtcUserBinaryNotice(self, unk1, capcom_id, offset, length, seq):
        """NtcUserBinaryNotice packet.

        ID: 66321000
        JP: ユーザ表示用バイナリ通知通知
        TR: User display binary notification notice
        """
        data = struct.pack(">B", unk1)
        data += pati.lp2_string(self.session.capcom_id)
        data += struct.pack(">I", offset)
        data += pati.lp2_string(self.session.hunter_info.pack()[offset:
                                                                offset+length])
        self.server.layer_broadcast(self.session, PatID4.NtcUserBinaryNotice,
                                    data, seq)

    def recvReqLayerDetailSearchHead(self, packet_id, data, seq):
        """ReqLayerDetailSearchHead packet.

        ID: 64900100
        JP: レイヤ検索詳細数要求
        TR: Layer detail search count request
        """
        with pati.Unpacker(data) as unpacker:
            self.search_info = {
                "layer": unpacker.struct(">B")[0],
                "search": unpacker.detailed_optional_fields(),
                "offset": unpacker.struct(">I")[0],
                "limit": unpacker.struct(">I")[0],
                "layer_fields": unpacker.bytes(),
                "user_fields": unpacker.bytes()
            }
        self.server.debug((
            "ReqLayerDetailSearchHead("
            "layer={layer!r}, search={search!r}, "
            "offset={offset}, limit={limit}, "
            "layer_fields={layer_fields!r}, user_fields={user_fields!r})"
        ).format(**self.search_info))
        self.sendAnsLayerDetailSearchHead(data, seq)

    def sendAnsLayerDetailSearchHead(self, data, seq):
        """AnsLayerDetailSearchHead packet.

        ID: 64900200
        JP: レイヤ検索詳細数返答
        TR: Layer detail search count response

        TODO: Find what to send.
        """
        unk1 = 0
        unk2 = 0
        self.search_data = self.session.layer_detail_search(
            self.search_info["search"]["data"]
        )
        count = len(self.search_data)
        data = struct.pack(">III", unk1, count, unk2)
        self.send_packet(PatID4.AnsLayerDetailSearchHead, data, seq)

    def recvReqLayerDetailSearchData(self, packet_id, data, seq):
        """ReqLayerDetailSearchData packet.

        ID: 64910100
        JP: レイヤ検索詳細データ要求
        TR: Layer detail search data request

        TODO: Handle this request.
        """
        offset, count = struct.unpack_from(">II", data)
        self.sendAnsLayerDetailSearchData(offset, count, seq)

    def sendAnsLayerDetailSearchData(self, offset, count, seq):
        """AnsLayerDetailSearchData packet.

        ID: 64910200
        JP: レイヤ検索詳細データ返答
        TR: Layer detail search data response

        TODO: Handle this response.
        """
        unk = 0
        cities = self.search_data
        data = struct.pack(">II", unk, len(cities))
        for i, city in enumerate(cities):
            with city.lock():
                layer_data = pati.LayerData.create_from(i, city)
                layer_data.assert_fields(self.search_info["layer_fields"])
                data += layer_data.pack()
                data += pati.pack_optional_fields(city.optional_fields)
                with city.players.lock():
                    data += struct.pack(">I", len(city.players))
                    for _, player in city.players:
                        layer_user = pati.LayerUserInfo()
                        layer_user.capcom_id = pati.String(player.capcom_id)
                        layer_user.hunter_name = pati.String(
                            player.hunter_name
                        )
                        layer_user.assert_fields(
                            self.search_info["user_fields"]
                        )
                        data += layer_user.pack()
                        data += pati.pack_optional_fields(
                            player.get_optional_fields()
                        )
        self.send_packet(PatID4.AnsLayerDetailSearchData, data, seq)

    def recvReqLayerDetailSearchFoot(self, packet_id, data, seq):
        """ReqLayerDetailSearchFoot packet.

        ID: 64920100
        JP: レイヤ検索詳細終了要求
        TR: Layer detail search end of transmission request
        """
        self.sendAnsLayerDetailSearchFoot(data, seq)

    def sendAnsLayerDetailSearchFoot(self, data, seq):
        """AnsLayerDetailSearchFoot packet.

        ID: 64920200
        JP: レイヤ検索詳細終了返答
        TR: Layer detail search end of transmission response
        """
        self.send_packet(PatID4.AnsLayerDetailSearchFoot, b"", seq)

    def recvReqLayerCreateHead(self, packet_id, data, seq):
        """ReqLayerCreateHead packet.

        ID: 64110100
        JP: レイヤ作成要求（番号指定）
        TR: Layer creation request (number specified)

        TODO: Lock it to prevent race-condition.
        """
        number, = struct.unpack(">H", data)
        self.sendAnsLayerCreateHead(number, seq)

    def sendAnsLayerCreateHead(self, number, seq):
        """AnsLayerCreateHead packet.

        ID: 64110200
        JP: レイヤ作成返答
        TR: Layer creation response
        """
        data = struct.pack(">H", number)
        if not self.session.is_city_empty(number):
            self.sendAnsAlert(PatID4.AnsLayerCreateHead,
                              "<LF=8><BODY><CENTER>City already exists.<END>",
                              seq)
            return
        if not self.session.reserve_city(number, True):
            self.sendAnsAlert(PatID4.AnsLayerCreateHead,
                              "<LF=8><BODY><CENTER>City reserved.<END>",
                              seq)
            return
        self.send_packet(PatID4.AnsLayerCreateHead, data, seq)

    def recvReqLayerCreateSet(self, packet_id, data, seq):
        """ReqLayerCreateSet packet.

        ID: 64120100
        JP: レイヤ作成設定要求（番号指定）
        TR: Layer creation settings request (number specified)
        """
        with pati.Unpacker(data) as unpacker:
            number, = unpacker.struct(">H")
            layer_set = unpacker.LayerSet()
            extra = unpacker.optional_fields()
        self.server.debug("LayerCreateSet: {}, {!r}, {!r}".format(
            number, layer_set, extra))
        self.sendAnsLayerCreateSet(number, layer_set, extra, seq)

    def sendAnsLayerCreateSet(self, number, layer_set, extra, seq):
        """AnsLayerCreateSet packet.

        ID: 64120200
        JP: レイヤ作成設定返答
        TR: Layer creation settings response
        """
        data = struct.pack(">H", number)
        self.session.layer_create(number, layer_set, extra)
        self.send_packet(PatID4.AnsLayerCreateSet, data, seq)

    def recvReqLayerCreateFoot(self, packet_id, data, seq):
        """ReqLayerCreateFoot packet.

        ID: 64130100
        JP: レイヤ作成完了要求（番号指定）
        TR: Layer creation end of transmission request
        """
        number, unk = struct.unpack(">HB", data)
        self.session.reserve_city(number, False)
        self.sendAnsLayerCreateFoot(number, unk, seq)

    def sendAnsLayerCreateFoot(self, number, unk, seq):
        """AnsLayerCreateFoot packet.

        ID: 64130200
        JP: レイヤ作成完了返答
        TR: Layer creation end of transmission response
        """
        data = struct.pack(">H", number)
        self.send_packet(PatID4.AnsLayerCreateFoot, data, seq)

    def recvReqLayerUp(self, packet_id, data, seq):
        """ReqLayerUp packet.

        ID: 64150100
        JP: レイヤアップ要求
        TR: Layer up request

        Sent by the game when leaving the gate via the entrance:
         - Relocate > Select Server
        """
        self.sendAnsLayerUp(data, seq)

    def sendAnsLayerUp(self, data, seq):
        """AnsLayerUp packet.

        ID: 64150200
        JP: レイヤアップ返答
        TR: Layer up response
        """
        self.session.layer_up()
        self.send_packet(PatID4.AnsLayerUp, b"", seq)

    def recvReqLayerMediationList(self, packet_id, data, seq):
        """ReqLayerMediationList packet.

        ID: 64820100
        JP: レイヤ調停データリスト取得要求
        TR: Get layer mediation list request
        """
        unk1, unk2 = struct.unpack_from(">BB", data)
        unk3 = data[2:]
        self.sendAnsLayerMediationList(unk1, unk2, unk3, seq)

    def sendAnsLayerMediationList(self, unk1, unk2, unk3, seq):
        """AnsLayerMediationList packet.

        ID: 64820200
        JP: レイヤ調停データリスト取得返答
        TR: Get layer mediation list response

        TODO: Store the item list and its state in the city.
        """
        unk = 0
        count = 14
        data = struct.pack(">BB", unk, count)
        for i in range(1, count+1):
            item = pati.MediationListItem()
            item.name = pati.String(b"Test")
            item.index = pati.Byte(i)
            item.is_locked = pati.Byte(0)
            data += item.pack()
        self.send_packet(PatID4.AnsLayerMediationList, data, seq)

    def recvReqLayerMediationLock(self, packet_id, data, seq):
        """ReqLayerMediationLock packet.

        ID: 64800100
        JP: レイヤ調停データ確保要求
        TR: Layer mediation data lock request

        Sent by the game when the player want to acquire a resource that
        cannot be shared by multiple players at the same time.
         - Seats are from index 1 to 12
         - Arm wrestling is from index 13 to 14
        """
        index, = struct.unpack_from(">B", data)
        mediation_data = pati.MediationListItem.unpack(data, 1)
        self.server.debug("LayerMediationLock: {}, {!r}".format(
            index, mediation_data))
        self.sendAnsLayerMediationLock(index, mediation_data, seq)

    def sendAnsLayerMediationLock(self, index, mediation_data, seq):
        """AnsLayerMediationLock packet.

        ID: 64800200
        JP: レイヤ調停データ確保返答
        TR: Layer mediation data lock response

        TODO: Enable notifications and handle player disconnection.
        """
        success = 1
        data = struct.pack(">B", success)
        # self.sendNtcLayerMediationLock(index, mediation_data, seq)
        self.send_packet(PatID4.AnsLayerMediationLock, data, seq)

    def sendNtcLayerMediationLock(self, index, mediation_data, seq):
        """NtcLayerMediationLock packet.

        ID: 64801000
        JP: レイヤ調停データ確保通知
        TR: Layer mediation data lock notification
        """
        data = pati.lp2_string(self.session.capcom_id)
        data += struct.pack(">B", index)
        data += mediation_data.pack()
        self.server.layer_broadcast(self.session,
                                    PatID4.NtcLayerMediationLock, data, seq)

    def recvReqLayerMediationUnlock(self, packet_id, data, seq):
        """ReqLayerMediationUnlock packet.

        ID: 64810100
        JP: レイヤ調停データ開放要求
        TR: Layer mediation data unlock request
        """
        index, = struct.unpack_from(">B", data)
        mediation_data = pati.MediationListItem.unpack(data, 1)
        self.server.debug("LayerMediationUnlock: {}, {!r}".format(
            index, mediation_data))
        self.sendAnsLayerMediationUnlock(index, mediation_data, seq)

    def sendAnsLayerMediationUnlock(self, index, mediation_data, seq):
        """AnsLayerMediationUnlock packet.

        ID: 64810200
        JP: レイヤ調停データ開放要求
        TR: Layer mediation data unlock response

        TODO: Enable notifications and handle player disconnection.
        """
        success = 1
        data = struct.pack(">B", success)
        # self.sendNtcLayerMediationUnlock(index, mediation_data, seq)
        self.send_packet(PatID4.AnsLayerMediationUnlock, data, seq)

    def sendNtcLayerMediationUnlock(self, index, mediation_data, seq):
        """NtcLayerMediationUnlock packet.

        ID: 64811000
        JP: レイヤ調停データ開放通知
        TR: Layer mediation data unlock notification
        """
        data = pati.lp2_string(self.session.capcom_id)
        data += struct.pack(">B", index)
        data += mediation_data.pack()
        self.server.layer_broadcast(self.session,
                                    PatID4.NtcLayerMediationUnlock, data, seq)

    def sendNtcLayerHost(self, new_leader, seq):
        """NtcLayerHost packet.

        ID: 64411000
        JP: レイヤのホスト通知
        TR: Layer host notification
        """
        data = struct.pack(">HII", 0x08, 0x00, 0x00)  # unk short array patitem
        data += pati.lp2_string(new_leader.capcom_id)
        data += pati.lp2_string(new_leader.hunter_name)
        self.server.layer_broadcast(self.session, PatID4.NtcLayerHost, data,
                                    seq)

    def sendNtcCircleHostHandover(self, circle, new_leader, new_leader_index,
                                  seq):
        """NtcCircleHostHandover packet.

        ID: 65401000
        JP: サークルのホスト移譲通知
        TR: Circle host transfer notice

        This packet is presently unused as it does not appear to have
        any valid callback function branch within Monster Hunter 3.
        """
        unk1 = 0
        data = struct.pack(">IB", unk1, new_leader_index + 1)
        data += pati.lp2_string(new_leader.capcom_id)
        data += pati.lp2_string(new_leader.hunter_name)
        data += pati.lp2_string(b"")  # Unk max-1 length short array
        self.server.circle_broadcast(circle, PatID4.NtcCircleHostHandover,
                                     data, seq, self.session)

    def sendNtcCircleHost(self, circle, new_leader, new_leader_index, seq):
        """NtcCircleHost packet.

        ID: 65411000
        JP: サークルのホスト通知
        TR: Circle host notification
        """
        unk1 = 0
        data = struct.pack(">IB", unk1, new_leader_index + 1)
        data += pati.lp2_string(new_leader.capcom_id)
        data += pati.lp2_string(new_leader.hunter_name)
        self.server.circle_broadcast(circle, PatID4.NtcCircleHost, data,
                                     seq, self.session)

    def notify_layer_departure(self):
        if self.session.layer == 2:
            new_host = self.session.try_transfer_city_leadership()
            if new_host:
                self.sendNtcLayerHost(new_host, 0)
        if self.session.layer > 0:
            ntc_data = pati.lp2_string(self.session.capcom_id)
            self.server.layer_broadcast(self.session, PatID4.NtcLayerOut,
                                        ntc_data, 0)
        if self.session.local_info['circle_id'] is not None:
            self.notify_circle_leave(self.session.local_info['circle_id'] + 1,
                                     seq=0)

    def notify_circle_leave(self, circle_index, seq):
        circle = self.session.get_circle()
        with circle.lock():
            self.sendNtcCircleLeave(circle, circle_index, seq)
            if circle.leader == self.session:
                if circle.departed:
                    new_host_index, new_host = \
                        self.session.try_transfer_circle_leadership()
                    if new_host:
                        self.sendNtcCircleHost(
                            circle, new_host, new_host_index, seq
                        )
                else:
                    self.sendNtcCircleBreak(circle, seq)
            self.session.leave_circle()
            self.sendNtcCircleListLayerChange(circle, circle_index, seq)

    def on_exception(self, e):
        # type: (Exception) -> None
        self.server.error(traceback.format_exc())
        self.send_error("{}: {}".format(type(e).__name__, str(e)))

    def on_finish(self):
        self.notify_layer_departure()
        self.session.layer_end()
        self.session.disconnect()
        self.session.delete()

        self.server.del_from_debug(self)
        self.server.info("Client finished!")

    def on_packet(self, data):
        if not data:
            self.finish()
            return

        packet_id, data, seq = data
        self.server.info(
            "RECV %s[ID=%08x; Seq=%04x]",
            PAT_NAMES.get(packet_id, "Packet"),
            packet_id, seq
        )
        self.server.debug("%s", hexdump(data))
        self.dispatch(packet_id, data, seq)

    def send_packet(self, packet_id=0, data=b'', seq=0):
        super(PatRequestHandler, self).send_packet(packet_id, data, seq)
        self.server.info(
            "SEND %s[ID=%08x; Seq=%04x]",
            PAT_NAMES.get(packet_id, "Packet"),
            packet_id, seq
        )
        self.server.debug("%s", hexdump(data))

    def dispatch(self, packet_id, data, seq):
        """Packet dispatcher."""
        if packet_id not in PAT_NAMES:
            self.server.error("Unknown packet ID: %08x", packet_id)
            return
        name = "recv{}".format(PAT_NAMES[packet_id])

        if not hasattr(self, name):
            self.server.error("Unsupported packet: %08x | %s", packet_id, name)
            return

        handler = getattr(self, name)
        return handler(packet_id, data, seq)

    def on_tick(self):
        if not self.requested_connection:
            # TODO: Investigate why do we need to wait a certain amount of
            #       seconds before sending the `ReqConnection` packet?
            if self.ping_timer.elapsed() >= 1.5:
                self.requested_connection = True
                self.sendReqConnection()
            return

        # Send a ping with 30 seconds interval
        if self.ping_timer.elapsed() >= 30:
            if not self.server.debug_enabled() and not self.line_check:
                raise Exception("Client timed out.")
            self.line_check = False
            self.sendReqLineCheck()
            self.ping_timer.restart()
