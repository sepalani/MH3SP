import ssl
import SocketServer


class MHTriSSLServer(SocketServer.TCPServer):
    """Generic SSL Server class for MHTri.

    Private key, certificate need to be generated in order for this server to work.
    """

    ssl_default = {
        'ssl_version': ssl.PROTOCOL_SSLv23,
        'keyfile': 'server.key',
        'certfile': 'server.crt',
        'server_side': True
    }

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, **kwargs):
        """Constructor.  May be extended, do not override."""
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        if len(kwargs) > 0:
            self.__ssl__(**kwargs)

    def __ssl__(self, **kwargs):
        """Setup an SSL connection. See ssl.wrap_socket documentation for the parameters."""
        for k in self.ssl_default:
            if k not in kwargs:
                kwargs[k] = self.ssl_default[k]
        self.socket = ssl.wrap_socket(self.socket, **kwargs)