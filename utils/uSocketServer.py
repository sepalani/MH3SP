#! /usr/bin/python
"""
Generic SocketServer module

Workaround for Python2 and Python3
"""
try:
    import SocketServer
except ImportError:
    import socketserver as SocketServer


class BaseServer(SocketServer.BaseServer):
    pass


class TCPServer(SocketServer.TCPServer):
    pass


class UDPServer(SocketServer.UDPServer):
    pass


class ForkingMixIn(SocketServer.ForkingMixIn):
    pass


class ThreadingMixIn(SocketServer.ThreadingMixIn):
    pass


class ForkingTCPServer(SocketServer.ForkingTCPServer):
    pass


class ForkingUDPServer(SocketServer.ForkingUDPServer):
    pass


class ThreadingTCPServer(SocketServer.ThreadingTCPServer):
    pass


class ThreadingUDPServer(SocketServer.ThreadingUDPServer):
    pass


class BaseRequestHandler(SocketServer.BaseRequestHandler):
    pass


class StreamRequestHandler(SocketServer.StreamRequestHandler):
    pass


class DatagramRequestHandler(SocketServer.DatagramRequestHandler):
    pass