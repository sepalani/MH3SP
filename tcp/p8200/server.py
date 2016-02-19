#! /usr/bin/python

import sys
import socket
import select
import threading
import Queue

from optparse import OptionParser

try:
    from utils.MHTriSSLServer import *
    import utils.uSocketServer as SocketServer
except ImportError:
    sys.path.append("../..")
    from utils.MHTriSSLServer import *
    import utils.uSocketServer as SocketServer

try:
    input = raw_input
except:
    pass


def prompt(handler):
    """Basic python prompt"""
    while handler.prompt_run:
        try:
            while handler.prompt_wait:
                if not handler.prompt_run:
                    break
            s = input("$> ")
            if not s:
                return
            handler.message_queue.put(str(eval(s)).encode('ascii'))
            handler.prompt_wait = True
        except (KeyboardInterrupt, EOFError) as e:
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
        print("[Server] Handle client")
        self.prompt_run = True
        self.prompt_wait = False
        self.message_queue = Queue.Queue()
        t = threading.Thread(target=prompt, args=(self,))
        t.start()

        while True:
            r, w, e = select.select([self.rfile], [self.wfile], [], 0.2123)
            if r:
                response = self.rfile.read()
                if not len(response):
                    break
                print("<<< %s" % response)
            if w:
                while not self.message_queue.empty():
                    message = self.message_queue.get()
                    self.wfile.write(message)
                    print(">>> %s" % message)
                else:
                    self.prompt_wait = False
            if e:
                break

        print("Press Enter to finish client")
        self.prompt_run = False
        t.join()
        print("Client finished!")


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-H", "--hostname", action="store", type=str,
                      default=socket.gethostname(), dest="host",
                      help="set server hostname")
    parser.add_option("-P", "--port", action="store", type=int,
                      default=8200, dest="port",
                      help="set server port")
    parser.add_option("-c", "--cert", action="store", type=str,
                      default='../../../server.crt', dest="cert",
                      help="set SSL server certificate")
    parser.add_option("-k", "--key", action="store", type=str,
                      default='../../../server.key', dest="key",
                      help="set SSL server private key")
    opt, arg = parser.parse_args()

    server = MHTriSSLServer((opt.host, opt.port), MHTriP8200RequestHandler)
    server.__ssl__(certfile=opt.cert, keyfile=opt.key)

    try:
        print("Server: %s | Port: %d" %
              (server.server_address[0], server.server_address[1]))
        server.serve_forever()
    except KeyboardInterrupt:
        print("[Server] Closing...")
        server.server_close()
