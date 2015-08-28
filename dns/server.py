#! /usr/bin/python

import sys
sys.path.append("..")

import socket
from utils.MHTriDNSServer import *
import utils.uSocketServer as SocketServer


def dns_pack(data, ip):
    """Pack DNS answer"""
    header = b"\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00"
    response = b"\xc0\x0c\x00\x01\x00\x01\x00\x00\x08\x47\x00\x04"
    answer = data[0:2] + header + data[12:]
    answer += response + socket.inet_aton(ip)
    return answer


class MHTriDNSRequestHandler(SocketServer.BaseRequestHandler):
    """Basic DNS request handler"""

    def handle(self):
        data = bytearray(self.request[0])
        sock = self.request[1]
        name = data.strip()[13:].split(b'\0')[0]
        s = "".join("." if c < 32 else chr(c) for c in name)
        print("<<< %s" % s)

        if s in self.server.record:
            s = self.server.record[s]
            if not s:
                s = self.server.server_address[0]

        try:
            ip = socket.gethostbyname(s)
            print(">>> %s" % ip)
            sock.sendto(dns_pack(data, ip), self.client_address)
        except socket.gaierror:
            pass


if __name__ == "__main__":
    """Usage:  python server.py [IP address]"""

    if len(sys.argv) > 1:
        hostname = sys.argv[1]
    else:
        hostname = socket.gethostname()
    HOST = socket.gethostbyname(hostname)
    PORT = 53
    server = MHTriDNSServer((HOST, PORT), MHTriDNSRequestHandler)

    try:
        print("Server: %s | Port: %d" % (server.server_address[0], server.server_address[1]))
        server.serve_forever()
    except KeyboardInterrupt:
        print("[Server] Closing...")
        server.server_close()
