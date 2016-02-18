import utils.uSocketServer as SocketServer


class MHTriDNSServer(SocketServer.UDPServer):
    """Generic DNS server class for MHTri.

    Empty record will point to server ip.
    """

    record = {
        'mh.capcom.co.jp': '',
        'mmh-t1-opn02.mmh-service.capcom.co.jp': '',
        'mmh-t1-opn03.mmh-service.capcom.co.jp': '',
        'mmh-t1-opn04.mmh-service.capcom.co.jp': '',
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
