#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2015-2021 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Monster Hunter DNS server."""

import socket

from other.utils import get_default_ip

try:
    # Python 3
    import socketserver as SocketServer
except ImportError:
    # Python 2
    import SocketServer


STR2HAX = ("97.74.103.14", "173.201.71.14")


class MHTriDNSServer(SocketServer.UDPServer):
    """Generic DNS server class for MHTri.

    Empty record will point to the server IP.
    """

    record = {
        "cfh.wapp.wii.com": STR2HAX,
        # Nintendo WFC
        "gpcm.gs.nintendowifi.net": "",
        "gpsp.gs.nintendowifi.net": "",
        "naswii.nintendowifi.net": "",
        "nas.nintendowifi.net": "",
        "gamestats.gs.nintendowifi.net": "",
        "gamestats2.gs.nintendowifi.net": "",
        "wiinat.available.gs.nintendowifi.net": "",
        "wiinat.natneg1.gs.nintendowifi.net": "",
        "wiinat.natneg2.gs.nintendowifi.net": "",
        "wiinat.natneg3.gs.nintendowifi.net": "",
        # Monster Hunter 3 (JAP)
        "monhunter3wii.gamestats.gs.nintendowifi.net": "",
        "monhunter3wii.gamestats2.gs.nintendowifi.net": "",
        "monhunter3wii.available.gs.nintendowifi.net": "",
        "monhunter3wii.natneg1.gs.nintendowifi.net": "",
        "monhunter3wii.natneg2.gs.nintendowifi.net": "",
        "monhunter3wii.natneg3.gs.nintendowifi.net": "",
        "monhunter3wii.master.gs.nintendowifi.net": "",
        "monhunter3wii.ms16.gs.nintendowifi.net": "",
        # Monster Hunter 3 (EU/US)
        "mh3uswii.available.gs.nintendowifi.net": "",
        "mh3uswii.natneg1.gs.nintendowifi.net": "",
        "mh3uswii.natneg2.gs.nintendowifi.net": "",
        "mh3uswii.natneg3.gs.nintendowifi.net": "",
        "mh3uswii.master.gs.nintendowifi.net": "",
        "mh3uswii.gamestats.gs.nintendowifi.net": "",
        "mh3uswii.gamestats2.gs.nintendowifi.net": "",
        "mh3uswii.ms1.gs.nintendowifi.net": "",
        # Wiimmfi
        "gpcm.gs.wiimmfi.de": "",
        "gpsp.gs.wiimmfi.de": "",
        "naswii.wiimmfi.de": "",
        "nas.wiimmfi.de": "",
        "gamestats.gs.wiimmfi.de": "",
        "gamestats2.gs.wiimmfi.de": "",
        "wiinat.available.gs.wiimmfi.de": "",
        "wiinat.natneg1.gs.wiimmfi.de": "",
        "wiinat.natneg2.gs.wiimmfi.de": "",
        "wiinat.natneg3.gs.wiimmfi.de": "",
        # Monster Hunter 3 (JAP)
        "monhunter3wii.gamestats.gs.wiimmfi.de": "",
        "monhunter3wii.gamestats2.gs.wiimmfi.de": "",
        "monhunter3wii.available.gs.wiimmfi.de": "",
        "monhunter3wii.natneg1.gs.wiimmfi.de": "",
        "monhunter3wii.natneg2.gs.wiimmfi.de": "",
        "monhunter3wii.natneg3.gs.wiimmfi.de": "",
        "monhunter3wii.master.gs.wiimmfi.de": "",
        "monhunter3wii.ms16.gs.wiimmfi.de": "",
        # Monster Hunter 3 (EU/US)
        "mh3uswii.available.gs.wiimmfi.de": "",
        "mh3uswii.natneg1.gs.wiimmfi.de": "",
        "mh3uswii.natneg2.gs.wiimmfi.de": "",
        "mh3uswii.natneg3.gs.wiimmfi.de": "",
        "mh3uswii.master.gs.wiimmfi.de": "",
        "mh3uswii.gamestats.gs.wiimmfi.de": "",
        "mh3uswii.gamestats2.gs.wiimmfi.de": "",
        "mh3uswii.ms1.gs.wiimmfi.de": "",
        # Capcom server
        "mh.capcom.co.jp": "",
        "mmh-t1-opn01.mmh-service.capcom.co.jp": "",
        "mmh-t1-opn02.mmh-service.capcom.co.jp": "",
        "mmh-t1-opn03.mmh-service.capcom.co.jp": "",
        "mmh-t1-opn04.mmh-service.capcom.co.jp": "",
    }

    def __init__(self, server_address, RequestHandlerClass,
                 bind_and_activate=True, record={}):
        SocketServer.UDPServer.__init__(self,
                                        server_address,
                                        RequestHandlerClass,
                                        bind_and_activate)
        if len(record) > 0:
            self.record = record

    def __len__(self):
        return len(self.record)

    def __getitem__(self, key):
        return self.record[key]

    def __setitem__(self, key, item):
        self.record[key] = item

    def __delitem__(self, key):
        del self.record[key]


def dns_pack(data, ip):
    """Pack DNS answer"""
    header = b"\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00"
    response = b"\xc0\x0c\x00\x01\x00\x01\x00\x00\x08\x47\x00\x04"
    answer = data[0:2] + header + data[12:]
    answer += response + socket.inet_aton(ip)
    return answer


class MHTriDNSRequestHandler(SocketServer.BaseRequestHandler):
    """Basic DNS request handler"""

    def forward(self, forwarders):
        if not self.server.str2hax:
            return None
        data, sock = self.request
        for dns_server in forwarders:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(data, (dns_server, 53))
            response, addrinfo = s.recvfrom(256)
            s.close()
            if not response:
                continue
            sock.sendto(response, self.client_address)
            print(">>> Forwarded via {}".format(dns_server))
            return True
        print("--- Failed to forward request!")

    def handle(self):
        data = bytearray(self.request[0])
        sock = self.request[1]
        name = data.strip()[13:].split(b'\0')[0]
        s = "".join("." if c < 32 else chr(c) for c in name)
        print("<<< {}".format(s))

        if s in self.server.record:
            record = self.server.record[s]
            if not record:
                s = get_default_ip()
            elif isinstance(record, tuple):
                if self.forward(record):
                    return  # Request forwarded successfully

        try:
            ip = socket.gethostbyname(s)
            print(">>> {}".format(ip))
            sock.sendto(dns_pack(data, ip), self.client_address)
        except socket.gaierror:
            pass


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-H", "--hostname", action="store", type=str,
                        default=get_default_ip(), dest="host",
                        help="set server hostname")
    parser.add_argument("-P", "--port", action="store", type=int,
                        default=53, dest="port",
                        help="set server port")
    parser.add_argument("--str2hax", action="store_true",
                        help="Enable str2hax forwarder")
    args = parser.parse_args()

    server = MHTriDNSServer((args.host, args.port), MHTriDNSRequestHandler)
    server.str2hax = args.str2hax
    if args.str2hax:
        print("!!!")
        print("!!! USE STR2HAX AT YOUR OWN RISK! THIS METHOD IS DISCOURAGED!")
        print("!!!  - IP(s): {}".format(", ".join(STR2HAX)))
        print("!!!")

    try:
        print("Server: {} | Port: {}".format(*server.server_address))
        server.serve_forever()
    except KeyboardInterrupt:
        print("[Server] Closing...")
        server.server_close()
