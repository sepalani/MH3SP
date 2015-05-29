#! /usr/bin/python

import sys
sys.path.append("../..")

import socket
from utils.MHTriSSLServer import *
import utils.uSocketServer as SocketServer


def prompt():
    """Basic python prompt"""
    while True:
        try:
            s = raw_input("$> ")
            if len(s) < 1:
                return
            yield eval(s)
        except (KeyboardInterrupt, EOFError, SyntaxError) as e:
            print("[Exiting prompt]")
            return
        except Exception as e:
            print("%s: %s" % (type(e).__name__, e))


class MHTriP8200RequestHandler(SocketServer.StreamRequestHandler):
    """Request Handler class for MHTri.
    
    Focus on port 8200 requests.
    ============================
     - First read [8 bytes]
       -> [0x00~0x01] Response size (uint16)
       -> [0x02~0x07] ???
    """
    def handle(self):
        """In-game buffer address
        
        PAL - 0x80CD5318 | Data read size: 0x80CD5310
        USA - 0x80CD5318 | Data read size: 0x80CD5310
        JAP - 0x80CA9400 | Data read size: 0x80CA93F8
        """
        for i in range(1):
            # Error 11602: Connection failed / Wrong pass phrase? / Server is running?
            # Error 11609: Connection closed unexpectedly [TCP: RST, ACK]
            # Error 11611: Connection closed by server [TCP: FIN, ACK] + [TCP: RST, ACK]
            # Error 11612: Wrong data sent
            # Error 11619: Timeout
            print("[Server] Handle client")
            for data in prompt():
                self.wfile.write(data)
                print(">>> %s" % (data))
        print("[Server] Waiting client...")
        print("<<< %s" % self.rfile.read())
        print("[Server] Finish client")


if __name__ == "__main__":
    """Usage:  python server.py [IP address]"""
    if len(sys.argv) > 1:
        hostname = sys.argv[1]
    else:
        hostname = socket.gethostname()
    HOST = socket.gethostbyname(hostname)
    PORT = 8200
    server = MHTriSSLServer((HOST, PORT), MHTriP8200RequestHandler)

    # Put the path of your private key/certificate
    server.__ssl__(certfile='../../../server.crt', keyfile='../../../server.key')
    try:
        print("Server: %s | Port: %d" % (server.server_address[0], server.server_address[1]))
        server.serve_forever()
    except KeyboardInterrupt:
        print("[Server] Closing...")
        server.server_close()
