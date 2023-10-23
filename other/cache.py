#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Monster Hunter cache module.

    Monster Hunter 3 Server Project
    Copyright (C) 2023  Ze SpyRo

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from mh.time_utils import Timer
from mh.session import Session
from mh.state import get_instance, Server
from other.utils import Logger, create_logger, get_remote_config, \
        get_central_config, get_config, get_ip

from threading import Lock, Event
import socket
import struct
import logging
import json

try:
    # Python 3
    import selectors
    from typing import Tuple, Union, Optional, Dict, List, Callable, TYPE_CHECKING
    if TYPE_CHECKING:
        from fmp_server import FmpRequestHandler
        from mh.pat_item import ConnectionData
except ImportError:
    # Python 2
    import externals.selectors2 as selectors


class PacketTypes(object):
    Ping = 0x0000
    FriendlyHello = 0x0001
    ReqConnectionInfo = 0x0002
    SendConnectionInfo = 0x0003
    ReqServerRefresh = 0x0004
    SessionInfo = 0x0005
    ServerIDList = 0x0006
    ServerShutdown = 0x0007
    SessionDisconnect = 0x0008


class CentralConnectionHandler(object):
    def __init__(self, sck, client_address, cache):
        # type: (socket.socket, Tuple[str, int], Cache) -> None
        self.id = -1  # type: int
        self.socket = sck
        self.client_address = client_address 
        self.cache = cache
        self.rfile = self.socket.makefile('rb', -1)
        self.wfile = self.socket.makefile('wb', 0)

        self.rw = Lock()
        self.finished = False  # type: bool

        self.handler_functions = {
            PacketTypes.Ping: self.RecvPing,
            PacketTypes.FriendlyHello: self.RecvFriendlyHello,
            PacketTypes.SendConnectionInfo: self.RecvConnectionInfo,
            PacketTypes.ReqConnectionInfo: self.RecvReqConnectionInfo,
            PacketTypes.ReqServerRefresh: self.RecvReqServerRefresh,
            PacketTypes.SessionInfo: self.RecvSessionInfo,
            PacketTypes.ServerShutdown: self.RecvServerShutdown,
            PacketTypes.SessionDisconnect: self.RecvSessionDisconnect
        }  # type: Dict[int, Callable[[int, bytes], None]]

    def fileno(self):
        # type: () -> int
        return self.socket.fileno()

    def on_recv(self):
        # type: () -> Optional[Tuple[int, int, bytes]]
        header = self.rfile.read(10)
        if not len(header) or len(header) < 10:
            return None

        return self.recv_packet(header)

    def recv_packet(self, header):
        # type: (bytes) -> Tuple[int, int, bytes]
        size, packet_id, server_id = struct.unpack(">IIH", header)
        data = self.rfile.read(size)
        return server_id, packet_id, data

    def send_packet(self, packet_id=0, data=b""):
        # type: (int, bytes) -> None
        self.wfile.write(self.pack_data(
            data, packet_id
        ))

    def pack_data(self, data, packet_id):
        # type: (bytes, int) -> bytes
        return struct.pack(">II", len(data), packet_id) + data

    def is_finished(self):
        # type: () -> bool
        return self.finished

    def on_exception(self, e):
        # type: (Exception) -> None
        self.finish()

    def direct_to_handler(self, packet):
        # type: (Tuple[int, int, bytes]) -> None
        server_id, packet_type, data = packet
        self.handler_functions[packet_type](server_id, data)

    def RecvPing(self, server_id, data):
        # type: (int, bytes) -> None
        pass

    def RecvFriendlyHello(self, server_id, data):
        # type: (int, bytes) -> None
        self.cache.debug("Recieved a friendly hello from {}!".format(
            server_id
        ))
        self.cache.register_handler(server_id, self)
        self.ReqConnectionInfo()

    def ReqConnectionInfo(self):
        # type: () -> None
        self.cache.debug("Requesting connection info.")
        self.send_packet(PacketTypes.ReqConnectionInfo, b"")

    def RecvConnectionInfo(self, server_id, data):
        # type: (int, bytes) -> None
        self.cache.debug("Recieved connection info sized {} from {}".format(
            len(data), server_id
        ))
        server = Server.deserialize(json.loads(data.decode('utf-8')))
        self.cache.servers[server_id] = server
        self.cache.update_players()

    def RecvReqConnectionInfo(self, server_id, data):
        # type: (int, bytes) -> None
        requested_server_id, = struct.unpack(">H", data)
        self.cache.debug("Recieved request for data of Server {}.".format(
            requested_server_id
        ))
        if server_id in self.cache.servers:
            data = json.dumps(self.cache.servers[server_id].serialize()).encode('utf-8')
            self.SendConnectionInfo(data)

    def SendConnectionInfo(self, data):
        # type: (bytes) -> None
        self.cache.debug("Sending updated connection info.")
        self.send_packet(PacketTypes.SendConnectionInfo, data)

    def RecvReqServerRefresh(self, server_id, data):
        # type: (int, bytes) -> None
        self.cache.debug("Recieved server refresh request from \
                          Server {}.".format(
            server_id
        ))
        self.SendServerIDList()
        for _server_id in self.cache.servers:
            data = struct.pack(">H", _server_id)
            data += json.dumps(self.cache.servers[_server_id].serialize()).encode('utf-8')
            self.SendConnectionInfo(data)

    def SendServerIDList(self):
        # type: () -> None
        self.cache.debug("Sending updated Server ID list.")
        data = struct.pack(">H", self.cache.servers_version)
        data += struct.pack(">H", len(self.cache.servers))
        for _server_id in self.cache.servers:
            data += struct.pack(">H", _server_id)
        self.send_packet(PacketTypes.ServerIDList, data)

    def RecvSessionInfo(self, server_id, data):
        # type: (int, bytes) -> None
        dest_server_id, = struct.unpack(">H", data[:2])
        self.cache.debug("Recieved session data from Server {} \
                            bound for Server {}.".format(
            server_id, dest_server_id
        ))
        self.cache.update_player_record(
            Session.deserialize(json.loads(data[2:].decode('utf-8')))
        )
        self.cache.get_handler(dest_server_id).SendSessionInfo(data[2:])

    def SendSessionInfo(self, ser_session):
        # type: (bytes) -> None
        self.cache.debug("Dispatching session info to remote Server.")
        self.send_packet(PacketTypes.SessionInfo, ser_session)

    def RecvServerShutdown(self, server_id, data):
        # type: (int, bytes) -> None
        raise Exception("Server shutting down.")

    def RecvSessionDisconnect(self, server_id, data):
        # type: (int, bytes) -> None
        length, = struct.unpack(">H", data[:2])
        capcom_id = str(data[2:2+length].decode('utf-8'))
        if capcom_id in self.cache.players:
            del self.cache.players[capcom_id]
            get_instance().update_players()

    def finish(self):
        # type: () -> None
        if self.finished:
            return

        self.finished = True

        try:
            self.wfile.close()
        except Exception:
            pass

        try:
            self.rfile.close()
        except Exception:
            pass

        try:
            self.socket.close()
        except Exception:
            pass


class RemoteConnectionHandler(object):
    def __init__(self, sck, client_address, cache):
        # type: (socket.socket, Tuple[str, int], Cache) -> None
        self.id = 0
        self.socket = sck
        self.client_address = client_address
        self.cache = cache
        self.rfile = self.socket.makefile('rb', -1)
        self.wfile = self.socket.makefile('wb', 0)

        self.rw = Lock()
        self.finished = False  # type: bool

        self.handler_functions = {
            PacketTypes.ReqConnectionInfo: self.ReqConnectionInfo,
            PacketTypes.SendConnectionInfo: self.RecvConnectionInfo,
            PacketTypes.SessionInfo: self.RecvSessionInfo,
            PacketTypes.ServerIDList: self.RecvServerIDList,
        }  # type: Dict[int, Callable[[bytes], None]]

    def fileno(self):
        # type: () -> int
        return self.socket.fileno()

    def on_recv(self):
         # type: () -> Optional[Tuple[int, bytes]]
        header = self.rfile.read(8)
        if not len(header) or len(header) < 8:
            return None

        return self.recv_packet(header)

    def recv_packet(self, header):
        # type: (bytes) -> Tuple[int, bytes]
        size, packet_id = struct.unpack(">II", header)
        data = self.rfile.read(size)
        return packet_id, data

    def is_finished(self):
        # type: () -> bool
        return self.finished

    def on_exception(self, e):
        # type: (Exception) -> None
        self.finish()

    def send_packet(self, packet_id=0, data=b""):
        # type: (int, bytes) -> None
        self.wfile.write(self.pack_data(
            data, packet_id
        ))

    def pack_data(self, data, packet_id):
        # type: (bytes, int) -> bytes
        return struct.pack(">IIH", len(data), packet_id,
                           self.cache.server_id) + data

    def direct_to_handler(self, packet):
        # type: (Tuple[int, bytes]) -> None
        packet_type, data = packet
        self.handler_functions[packet_type](data)

    def SendFriendlyHello(self, data=b""):
        # type: (bytes) -> None
        self.cache.debug("Sending a friendly hello!")
        self.send_packet(PacketTypes.FriendlyHello, data)

    def ReqConnectionInfo(self, data):
        # type: (bytes) -> None
        self.cache.debug("Recieved request for update connection info from Central.")
        server = get_instance().server
        assert server != None

        data = json.dumps(server.serialize()).encode('utf-8')
        self.SendConnectionInfo(data)

    def SendConnectionInfo(self, data):
        # type: (bytes) -> None
        self.cache.debug("Sending connection info to Central.")
        self.send_packet(PacketTypes.SendConnectionInfo, data)

    def SendReqServerRefresh(self):
        # type: () -> None
        self.cache.debug("Requesting refreshed server info from central.")
        self.send_packet(PacketTypes.ReqServerRefresh, b"")

    def SendReqConnectionInfo(self, server_id):
        # type: (int) -> None
        self.cache.debug("Requesting info for Server {}".format(
            server_id
        ))
        self.send_packet(PacketTypes.ReqConnectionInfo,
                         struct.pack(">H", server_id))

    def RecvServerIDList(self, data):
        # type: (bytes) -> None
        self.cache.debug("Recieved updated Server ID list from Central.")
        servers_version, count = struct.unpack(">HH", data[:4])
        self.cache.update_servers_version(servers_version)
        updated_server_ids = []
        for i in range(count):
            server_id = struct.unpack(">H", data[2*(i+2):2*(i+2)+2])
            updated_server_ids.append(server_id)
        for server_id in self.cache.servers.keys():
            if server_id not in updated_server_ids:
                self.cache.prune_server(server_id)

    def RecvConnectionInfo(self, data):
        # type: (bytes) -> None
        try:
            server_id, = struct.unpack(">H", data[:2])
            server = Server.deserialize(json.loads(data[2:].decode('utf-8')))
        except Exception as e:
            self.cache.error(e)
            return
        self.cache.debug("Obtained updated server info for Server {}".format(
            server_id
        ))
        self.cache.servers[server_id] = server

    def SendSessionInfo(self, server_id, ser_session):
        # type: (int, bytes) -> None
        self.cache.debug("Sending Session info to Server {}".format(
            server_id
        ))
        data = struct.pack(">H", server_id)
        data += ser_session
        self.send_packet(PacketTypes.SessionInfo, data)

    def RecvSessionInfo(self, data):
        # type: (bytes) -> None
        self.cache.debug("Recieved new Session info!")
        self.cache.new_session(Session.deserialize(json.loads(data.decode('utf-8'))))

    def SendSessionDisconnect(self, capcom_id):
        # type: (bytes) -> None
        data = struct.pack(">H", len(capcom_id))
        data += capcom_id.encode('utf-8')
        self.send_packet(PacketTypes.SessionDisconnect, data)

    def finish(self):
        # type: () -> None
        if self.finished:
            return

        self.finished = True

        try:
            self.wfile.close()
        except Exception:
            pass

        try:
            self.rfile.close()
        except Exception:
            pass

        try:
            self.socket.close()
        except Exception:
            pass


class Cache(Logger):
    def __init__(self, server_id, debug_mode=False, log_to_file=False,
                 log_to_console=False, log_to_window=False,
                 refresh_period=30, ssl_location='cert/crossserverCA/'):
        # type: (int, bool, bool, bool, bool, int, str) -> None
        Logger.__init__(self)
        self.servers_version = 1  # type: int
        self.servers = {
            # To be populated by remote connection
        }  # type: Dict[int, Server]

        self.outbound_sessions = [
            # (destination_server_id, session)
        ]  # type: List[Tuple[int, bytes]]

        self.players = {
            # capcom_id -> connectionless sessions from other servers
        }  # type: Dict[str, Session]
        self.ready_sessions = {
            # pat_ticket -> True or connection_data
        }  # type: Dict[str, Union[bool, Tuple[FmpRequestHandler, ConnectionData, int]]]

        log_level = logging.DEBUG if debug_mode else logging.INFO
        log_file = "cache.log" if log_to_file else ""

        self.set_logger(create_logger("Cache", log_level, log_file, log_to_console, log_to_window))

        self.is_central_server = server_id == 0
        if not self.is_central_server:
            remote_config = get_remote_config("SERVER{}".format(server_id))
            get_instance().setup_server(server_id,
                                        remote_config["Name"],
                                        int(remote_config["ServerType"]),
                                        int(remote_config["Capacity"]),
                                        get_ip(remote_config["IP"]),
                                        int(remote_config["Port"]))
        else:
            config = get_config("FMP")
            get_instance().setup_server(
                server_id, "", 0, 1, '0.0.0.0', config["Port"]
            )
        self.shut_down = False  # type: bool
        self.shut_down_event = Event()
        self.refresh_period = refresh_period
        self.handlers = {}  # type: Dict[int, CentralConnectionHandler]
        self.pending_connections = {} # type: Dict[CentralConnectionHandler, Timer]
        self.remote_server = None # type: Optional[RemoteConnectionHandler]
        self.server_id = server_id
        self.central_config = get_central_config()
        self.central_connection = (self.central_config["CentralIP"],
                                   self.central_config["CentralCrossconnectPort"])
        self.sel = selectors.DefaultSelector()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ssl_location = ssl_location
        if self.central_config["CrossconnectSSL"]:
            self.create_ssl_wrapper()

    def create_ssl_wrapper(self):
        # type: () -> None
        import ssl
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        if self.is_central_server:
            context.load_verify_locations(
                cafile="{}ca.crt".format(self.ssl_location)
            )
            context.load_cert_chain("{}MH3SP.crt".format(self.ssl_location),
                                    "{}MH3SP.key".format(self.ssl_location))
        else:
            context.load_cert_chain(
                "{}client{}.crt".format(self.ssl_location, self.server_id),
                "{}client{}.key".format(self.ssl_location, self.server_id)
            )
        self.socket = context.wrap_socket(
            self.socket, server_side=self.is_central_server
        )

    def update_player_record(self, session):
        # type: (Session) -> None
        get_instance().update_capcom_id(session)

    def update_players(self):
        # type: () -> None

        players = []
        for server_id, server in self.servers.items():
            if server_id != self.server_id:
                players = players + server.get_all_players()
        new_players = {}
        for p in players:
            new_players[p.capcom_id] = p
        self.players = new_players
        if self.is_central_server:
            get_instance().update_players()

    def get_remote_players_list(self):
        # type: () -> List[Session]
        players = []
        for server_id, server in self.servers.items():
            if server_id != self.server_id:
                players = players + server.get_all_players()
        return players

    def update_servers_version(self, servers_version):
        # type: (int) -> None
        self.servers_version = servers_version

    def get_server_list(self, include_ids=False):
        # type: (bool) -> Union[List[Server], Tuple[List[int], List[Server]]]
        if include_ids:
            return list(self.servers.keys()), list(self.servers.values())
        return list(self.servers.values())

    def get_server(self, server_id):
        # type: (int) -> Server
        assert server_id in self.servers
        return self.servers[server_id]

    def send_session_info(self, server_id, session):
        # type: (int, Session) -> None
        self.outbound_sessions.append(
            (server_id, json.dumps(session.serialize()).encode('utf-8'))
        )

    def new_session(self, session):
        # type: (Session) -> None
        pat_ticket = session.pat_ticket
        assert pat_ticket is not None
        
        ready_data = self.session_ready(pat_ticket)
        if ready_data:
            self.set_session_ready(pat_ticket, False)
            get_instance().register_pat_ticket(session)
            self.send_login_packet(*ready_data) # type: ignore
        else:
            self.set_session_ready(pat_ticket, session)

    def session_ready(self, pat_ticket):
        # type: (str) -> Union[bool, Tuple[FmpRequestHandler, ConnectionData, int]]
        return self.ready_sessions.get(pat_ticket, False)

    def set_session_ready(self, pat_ticket, store_data):
        # type: (str, Union[bool, Tuple[FmpRequestHandler, ConnectionData, int]]) -> None
        self.ready_sessions[pat_ticket] = store_data

    def notify_session_deletion(self, capcom_id):
        # type: str -> None
        if not self.is_central_server:
            self.remote_server.SendSessionDisconnect(capcom_id)

    def send_login_packet(self, player_handler, connection_data, seq):
        # type: (FmpRequestHandler, ConnectionData, int) -> None
        player_handler.sendNtcLogin(3, connection_data, seq)

    def get_handler(self, server_id):
        # type: (int) -> CentralConnectionHandler
        return self.handlers[server_id]

    def register_handler(self, server_id, handler):
        # type: (int, CentralConnectionHandler) -> None
        handler.id = server_id
        del self.pending_connections[handler]
        self.handlers[server_id] = handler

    def prune_server(self, server_id):
        # type: (int) -> None
        for player in self.servers[server_id].get_all_players():
            if player.capcom_id in self.players:
                del self.players[player.capcom_id]
        if server_id != 0:
            del self.servers[server_id]
        if self.is_central_server:
            self.update_servers_version(self.servers_version + 1)

    def maintain_connection(self):
        # type: () -> None
        state = get_instance()
        state.initialized.wait()
        state.cache = self

        refresh_timer = Timer()
        if self.is_central_server:
            # CENTRAL SERVER CONNECTION TO REMOTE
            self.serve_cache(refresh_timer)
        else:
            # REMOTE SERVER CONNECTION TO CENTRAL
            self.remote_connection_to_central_server(refresh_timer)

    def remote_connection_to_central_server(self, refresh_timer):
        # type: (Timer) -> None
        central_host = "localhost" if self.central_connection[0] == "0.0.0.0" else self.central_connection[0]
        central_addr = (central_host, self.central_connection[1])

        while not self.shut_down:
            # Connect to the central server if needed
            if self.remote_server is None or self.remote_server.is_finished():
                self.info("Connecting to central server at {}:{}...".format(central_addr[0], central_addr[1]))

                if self.remote_server is not None:
                    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    if self.central_config["CrossconnectSSL"]:
                        self.create_ssl_wrapper()
                    self.remote_server = None

                connect_timer = Timer()
                try:
                    self.socket.settimeout(60.0)
                    self.socket.connect(central_addr)
                    self.socket.settimeout(None)
                except socket.error as sck_error:
                    self.error("Failed! {}.".format(sck_error))
                    if connect_timer.elapsed() < 60.0:
                        remaining = 60.0 - connect_timer.elapsed()
                        self.debug("Retrying in {:.2f}s".format(remaining))
                        self.shut_down_event.wait(remaining)
                    continue

                self.remote_server = RemoteConnectionHandler(self.socket, central_addr, self)
                self.sel.register(self.remote_server, selectors.EVENT_READ | selectors.EVENT_WRITE)

            try:
                # Listen for incoming packets
                assert self.remote_server is not None
                events = self.sel.select(timeout=1)
                for _, event in events:
                    if bool(event & selectors.EVENT_WRITE):
                        self.remote_server.SendFriendlyHello()
                        self.sel.modify(self.remote_server, selectors.EVENT_READ)
                    elif bool(event & selectors.EVENT_READ):
                        packet = self.remote_server.on_recv()
                        if packet is None:
                            continue
                        self.remote_server.direct_to_handler(packet)
                # Request updated server information
                if refresh_timer.elapsed() >= self.refresh_period:
                    assert self.remote_server is not None
                    try:
                        self.remote_server.SendReqServerRefresh()
                    finally:
                        refresh_timer.restart()
                #  Pass on an outbound session
                if len(self.outbound_sessions) > 0:
                    self.debug("Outbound Session dispatching to Central Server.")
                    assert self.remote_server is not None
                    self.remote_server.SendSessionInfo(*self.outbound_sessions.pop(0))
            except Exception as exc:
                assert self.remote_server is not None
                self.remote_server.on_exception(exc)
            finally:
                assert self.remote_server is not None
                if not self.shut_down and self.remote_server.is_finished():
                    self.sel.unregister(self.remote_server)


    def serve_cache(self, refresh_timer):
        # type: (Timer) -> None
        try:
            self.socket.bind(self.central_connection)
            self.socket.listen(0)
        except socket.error as sck_error:
            self.error('Failed to bind server to {}:{}. {}'.format(self.central_connection[0], self.central_connection[1], sck_error))
            return
        self.info("Listening for remote servers on {}:{}".format(self.central_connection[0], self.central_connection[1]))
        self.sel.register(self.socket, selectors.EVENT_READ)

        while not self.shut_down:
            events = self.sel.select(timeout=1)
            # Respond to incoming packets
            for key, event in events:
                connection = key.fileobj
                if connection == self.socket:
                    # Accept a new connection
                    new_client = None
                    try:
                        new_client = self.socket.accept()
                    except Exception as exc:
                        self.error("Failed to accept incoming connection. {}".format(
                            exc))
                        continue
                    
                    client_socket, client_address = new_client
                    self.info("Remote Server connected from {}".format(
                        client_address
                    ))
                    handler = CentralConnectionHandler(client_socket,
                                                       client_address,
                                                       self)
                    self.pending_connections[handler] = Timer()
                    self.sel.register(handler, selectors.EVENT_READ)
                    self.update_servers_version(self.servers_version + 1)
                else:
                    assert event == selectors.EVENT_READ
                    assert isinstance(connection, CentralConnectionHandler)
                    try:
                        packet = connection.on_recv()
                        if packet is None:
                            if connection.is_finished():
                                self.remove_handler(connection)
                            continue
                        connection.direct_to_handler(packet)
                    except Exception as exc:
                        connection.on_exception(exc)
                        if not connection.is_finished():
                            continue
                        self.info(
                            "Connection to Remote Server {} lost: {}.".format(
                            connection.id,
                            exc
                        ))
                        self.remove_handler(connection)
            if refresh_timer.elapsed() >= self.refresh_period:
                for _, handler in self.handlers.items():
                    try:
                        handler.ReqConnectionInfo()
                    except Exception as exc:
                        handler.on_exception(exc)

                    if handler.is_finished():
                        self.remove_handler(handler)
                refresh_timer.restart()
            # Pass on an outbound session
            if len(self.outbound_sessions) > 0:
                self.debug("Session outbound...")
                outbound_session = self.outbound_sessions.pop(0)
                self.debug("Dispatching Session to Server {}.".format(
                    outbound_session[0]
                ))

                server_handler = self.get_handler(outbound_session[0])

                try:
                    server_handler.SendSessionInfo(outbound_session[1])
                except Exception as exc:
                    server_handler.on_exception(exc)

                if server_handler.is_finished():
                    self.remove_handler(server_handler)
            # Prune dangling pending connection
            for handler, timer in self.pending_connections.items():
                if timer.elapsed() < 30.0:
                    continue
                self.warning('Prunning dangling remote server connection {}:{}'.format(handler.client_address[0], handler.client_address[1]))
                try:
                    handler.finish()
                except Exception:
                    pass
                self.sel.unregister(handler)
                del self.pending_connections[handler]

    def remove_handler(self, handler):
        # type: (CentralConnectionHandler) -> None
        if handler.id > -1:
            try:
                del self.handlers[handler.id]
            except KeyError:
                pass
        else:
            try:
                del self.pending_connections[handler]
            except KeyError:
                pass

        try:
            self.sel.unregister(handler)
        except KeyError:
            pass

        try:
            handler.finish()
        except Exception:
            pass

        if handler.id > -1:
            self.prune_server(handler.id)

        if self.is_central_server:
            for handler in self.handlers.values():
                try:
                    handler.SendServerIDList()
                except Exception:
                    self.error("Failed to send the Server ID list to a handler.")

    def close(self):
        # type: () -> None
        if self.shut_down:
            return

        self.shut_down = True
        self.shut_down_event.set()

        if self.is_central_server:
            for _, handler in self.handlers.items():
                try:
                    handler.finish()
                except Exception:
                    pass

            self.handlers.clear()

            for handler, _ in self.pending_connections.items():
                try:
                    handler.finish()
                except Exception:
                    pass
            self.pending_connections.clear()
        elif self.remote_server is not None:
            try:
                self.remote_server.send_packet(PacketTypes.ServerShutdown, b"")
            except Exception:
                pass

            try:
                self.remote_server.finish()
            except Exception:
                pass

        self.socket.close()
        self.sel.close()

        self.info('Server Closed')
