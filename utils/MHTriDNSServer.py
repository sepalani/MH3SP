import utils.uSocketServer as SocketServer


class MHTriDNSServer(SocketServer.UDPServer):
    """Generic DNS server class for MHTri.

    Empty record will point to server ip.
    """

    record_a = {
        'mh.capcom.co.jp': '',
        'mmh-t1-opn02.mmh-service.capcom.co.jp': '',
        'mmh-t1-opn03.mmh-service.capcom.co.jp': '',
        'mmh-t1-opn04.mmh-service.capcom.co.jp': '',
    }

    record = {}

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, record={}):
        SocketServer.UDPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        if len(record) > 0:
            MHTriDNSServer.record = record
        else:
            MHTriDNSServer.record = self.record_a

    def __len__(self):
        return len(self.record) 

    def __getitem__(self, key):
        return self.record[key]

    def __setitem__(self, key, item):
        self.record[key] = item 

    def __delitem__(self, key):
        del self.record[key]