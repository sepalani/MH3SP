#! /usr/bin/python

import sys
sys.path.append("../..")

from utils.MHTriSSLServer import *
import SocketServer


def prompt():
    """Basic python prompt"""
    s = raw_input("$> ")
    if len(s) > 0:
        try:
            return eval(s)
        except Exception, e:
            print "Raised Exception:", e
            return prompt()
    else:
        return None


class MHTriP8200RequestHandler(SocketServer.StreamRequestHandler):
    """Request Handler class for MHTri.
    
    Focus on port 8200 requests.
    ============================
     - First read [8 bytes]
       -> [0x00] Number of block?
       -> [0x01~0x07] ???
       *** Block Size = ~256 bytes
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
            print "[Server] Handle client"
            data = prompt()
            while data is not None:
                self.wfile.write(data)
                print ">>> %s" % (data)
                data = prompt()
        print "[Server] Waiting client..."
        print "<<< %s" % self.rfile.read()
        print "[Server] Finish client"


if __name__ == "__main__":
    HOST, PORT = '', 8200
    server = MHTriSSLServer((HOST, PORT), MHTriP8200RequestHandler)

    # Put the path of your private key/certificate
    server.__ssl__(certfile='../../../server.crt', keyfile='../../../server.key')
    try:
        print "Server: %s | Port: %d" % (server.server_address[0], server.server_address[1])
        server.serve_forever()
    except KeyboardInterrupt:
        print "[Server] Closing..."
        server.server_close()