#! /usr/bin/python

import sys
sys.path.append("../..")

from utils.MHTriSSLServer import *
import SocketServer


class MHTriP8200RequestHandler(SocketServer.StreamRequestHandler):
    """Request Handler class for MHTri.
    
    Focus on port 8200 requests.
    """
    def handle(self):
        for i in range(1):
            # Error 11602: Connection failed / Wrong pass phrase? / Server is running?
            # Error 11609: Connection closed unexpectedly
            # Error 11612: Wrong data sent
            # Error 11619: Timeout
            print("[Server] Handle client")
            head = chr(0) * 8
            data = raw_input("$>")
            self.wfile.write(head + data)
            print(">>> %s" % (head + data))
        print("<<< %s" % self.rfile.read())
        print("[Server] Finish client")


if __name__ == "__main__":
    HOST, PORT = '', 8200
    server = MHTriSSLServer((HOST, PORT), MHTriP8200RequestHandler)

    # Put the path of your private key/certificate
    server.__ssl__(certfile='../../../server.crt', keyfile='../../../server.key')
    try:
        print("Server: %s | Port: %d" % (server.server_address[0], server.server_address[1]))
        server.serve_forever()
    except KeyboardInterrupt:
        print("[Server] Closing...")
        server.server_close()