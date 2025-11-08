#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2025 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Network utils module."""

import os
import socket
import ssl
import struct
import sys
import traceback

from other.python import PYTHON_VERSION, TYPE_CHECKING
from threading import Event

if PYTHON_VERSION == 3:
    import selectors
    from socketserver import StreamRequestHandler, TCPServer
elif not TYPE_CHECKING:
    import externals.selectors2 as selectors
    from SocketServer import \
        StreamRequestHandler as StreamRequestHandler_, \
        TCPServer as TCPServer_

    # Fix Python2 issue with super()
    # noinspection PyMissingOrEmptyDocstring
    class TCPServer(object, TCPServer_):
        pass

    # noinspection PyMissingOrEmptyDocstring
    class StreamRequestHandler(object, StreamRequestHandler_):
        pass
else:
    import selectors
    from socketserver import StreamRequestHandler, TCPServer
    from typing import Any, Self, TypeAlias  # noqa: F401
    IpAddress = str
    Port = int
    ClientAddress = tuple[IpAddress, Port]
    ServerAddress = tuple[IpAddress, Port]
    SelectorsEvents = list[tuple[selectors.SelectorKey, int]]


class SelectorsRequestHandler(StreamRequestHandler):
    """Custom StreamRequestHandler with selectors support.

    It differs from the regular StreamRequestHandler as it needs to maintain
    the socket connection. It will call the handler's `setup` method but won't
    call its `handle` and `finish` methods to keep it alive.

    N.B.: In this context, `finish` refers to the RequestHandler class. So the
    `finish` method should be used to clean up resources this class created.
    The server class is still responsible for cleaning up the request/socket.

    Class variables that may be overridden:
     - rbufsize
     - wbufsize
     - timeout
     - disable_nagle_algorithm
    """

    # noinspection PyMissingConstructor
    def __init__(self, request, client_address, server):
        # type: (socket.socket, ClientAddress, SelectorsBaseServer) -> None
        """See socketserver.py source code for more information."""
        self.request = request
        self.client_address = client_address
        self.server = server
        self.__finished = False
        self.setup()

    def __str__(self):
        # type: () -> str
        """Custom string representation."""
        return "{}({}:{})".format(self.__class__.__name__,
                                  *self.client_address)

    def fileno(self):
        # type: () -> int
        """Return the associated socket file descriptor."""
        return self.connection.fileno()

    def handle(self):
        # type: () -> None
        """Handle a single incoming request."""
        raise NotImplementedError("must be implemented in subclass")

    def finish(self):
        # type: () -> None
        """Terminate the request handler.

        MUST BE CALLED if overridden, failing to do so will disrupt the
        `is_finished` method.

        MUST NOT RAISE EXCEPTIONS.
        """
        self.__finished = True
        try:
            super(SelectorsRequestHandler, self).finish()
        except socket.error as e:
            # Closing wfile can sometimes raise an exception.
            self.on_exception(e)

    def is_finished(self):
        # type: () -> bool
        """Check whether the connection is active."""
        # return self.wfile.closed
        #  ^ Not sure the above is reliable if super().finish() throws.
        return self.__finished

    def on_recv(self):
        # type: () -> Any
        """Selectors read event callback."""
        pass

    def on_send(self):
        # type: () -> None
        """Selectors write event callback."""
        pass

    def on_exception(self, e):
        # type: (BaseException) -> None
        """Error callback that the server should call on error.

        MUST NOT RAISE EXCEPTIONS.
        """
        pass


class InvalidHeader(Exception):
    """PacketHandler invalid header exception."""
    pass


class PacketHandler(SelectorsRequestHandler):
    """SelectorsRequestHandler with packet specialization.

    The default packet format is as follows (RequestHeader + data):
     - (uint16_t) packet_size
     - (uint16_t) packet_sequence
     - (uint32_t) packet_id
     - (bytes) packet_data
    """

    HEADER_SIZE = 8
    PACKET_FORMAT = ">HHI"

    if TYPE_CHECKING:
        PacketSeq = int  # type: TypeAlias
        PacketId = int  # type: TypeAlias
        RequestHeader = tuple[int, PacketSeq, PacketId]  # size, sequence, id
        RequestPacket = tuple[PacketSeq, PacketId, bytes]  # sequence, id, data
        # ^ Ideally, should be: tuple[*RequestHeader[1:], bytes]

    def handle(self):
        # type: () -> None
        """Handle a single incoming packet."""
        packet = self.on_recv()
        if packet:
            self.handle_packet(*packet)
        else:
            self.finish()

    def on_recv(self):
        # type: () -> None | PacketHandler.RequestPacket
        """When read is available, check for incoming packet header."""
        header = self.rfile.read(self.HEADER_SIZE)
        if not header:
            # The socket was closed
            return None

        if len(header) < self.HEADER_SIZE:
            # Invalid packet header
            raise InvalidHeader(header)

        return self.recv_packet(header)

    def on_exception(self, e):
        # type: (BaseException) -> None
        """Close the connection on error.

        Example:
        ```
        if isinstance(e, (socket.error, InvalidHeader)):
            # Implement error handling here
        ```

        Reminder: MUST NOT RAISE EXCEPTIONS.
        """
        if not self.is_finished():
            # TODO: On non-fatal exception shouldn't we ignore it instead?
            # noinspection PyBroadException
            try:
                self.finish()
            except Exception:
                pass

    def recv_packet(self, data):
        # type: (bytes) -> PacketHandler.RequestPacket
        """Receive packet based on the provided header data."""
        header = struct.unpack(self.PACKET_FORMAT,
                               data)  # type: PacketHandler.RequestHeader
        packet_size = header[0]
        data = self.rfile.read(packet_size)
        return header[1:] + (data,)

    def send_packet(self, *args):
        # type: (*Any) -> None
        """Construct and send packet header and data."""
        params = args[:-1]
        data = args[-1]
        self.wfile.write(struct.pack(self.PACKET_FORMAT, len(data), *params))
        if data:
            self.wfile.write(data)

    def handle_packet(self, *args):
        # type: (*Any) -> None
        """Called when a packet is received.

        It takes as arguments the unpacked RequestHeader (except its size) and
        the received data.
        """
        raise NotImplementedError("must be implemented in subclass")


class SelectorsBaseServer(TCPServer):
    """Custom BaseServer with selectors support.

    Compared to the original BaseServer, this implementation also monitors
    request handler class using selectors.select().

    While SocketServer's MixIn might work, they shouldn't be used because
    they handle each request individually preventing them to be monitored
    continuously.

    Class variables that may be overridden:
     - request_queue_size
     - allow_reuse_address
     - allow_reuse_port  # Python 3 only

    Instance variables:
     - server_address
     - handler_class
     - socket
     - selector
     - args
     - kwargs
    """

    request_queue_size = 0
    if os.name != "nt":
        # Windows SO_REUSEADDR behaves differently
        # (e.g. allows 2 servers to bind+listen on the same address:port)
        # TODO: Confirm this behaviour on old versions of Windows (XP ~ 7)
        allow_reuse_address = True

    # noinspection PyMissingConstructor
    def __init__(self, server_address, handler_class, *args, **kwargs):
        # type: (ServerAddress, type[SelectorsRequestHandler], Any, Any) -> None  # noqa: E501
        """Custom flexible constructors."""
        self.server_address = server_address
        self.handler_class = handler_class  # type: type[SelectorsRequestHandler]  # noqa: E501
        self.socket = socket.socket(self.address_family, self.socket_type)
        self.selector = selectors.DefaultSelector()
        self.args = args
        self.kwargs = kwargs
        self.__is_shut_down = Event()
        self.__shutdown_request = False
        try:
            self.server_bind()
            self.server_activate()
        except:  # All errors  # noqa: E722
            self.server_close()
            raise

    def __enter__(self):
        # type: () -> Self
        return self

    def __exit__(self, *args):
        # type: (Any) -> None
        self.server_close()

    def __on_connection(self):
        # type: () -> None
        """Handle a new connection when the server socket is readable."""
        try:
            request, client_address = self.get_request()
        except socket.error:
            self.handle_error()
            return

        # noinspection PyBroadException
        try:
            if self.verify_request(request, client_address):
                self.process_request(request, client_address)
            else:
                self.shutdown_request(request)
        except Exception:
            self.handle_error(request, client_address)
            self.shutdown_request(request)
        except:  # Fatal error  # noqa: E722
            self.shutdown_request(request)
            raise

    def __on_read_event(self, handler):
        # type: (SelectorsRequestHandler) -> None
        """Handle request handler read events."""
        # noinspection PyBroadException
        try:
            handler.handle()
        except Exception:
            self.handle_error(handler, handler.client_address)
        finally:
            if handler.is_finished():
                self.shutdown_request(handler)

    def __on_write_event(self, handler):
        # type: (SelectorsRequestHandler) -> None
        """Handle request handler write events.

        N.B.: Not monitored by default.
        """
        # noinspection PyBroadException
        try:
            handler.on_send()
        except Exception:
            self.handle_error(handler, handler.client_address)

    def __handle_events(self, events, n=None):
        # type: (SelectorsEvents, None | int) -> None
        """Handle at most `n` events and call service_actions."""
        try:
            for key, mask in events[:n]:
                obj = key.fileobj
                if obj == self and mask & selectors.EVENT_READ:
                    self.__on_connection()
                    continue
                assert isinstance(obj, SelectorsRequestHandler)
                if mask & selectors.EVENT_READ:
                    self.__on_read_event(obj)
                if mask & selectors.EVENT_WRITE:
                    self.__on_write_event(obj)
        finally:
            self.service_actions()

    def get_handlers(self):
        # type: () -> list[SelectorsRequestHandler]
        """Create a new list populated with monitored handlers."""
        handlers = []  # type: list[SelectorsRequestHandler]
        mapping = self.selector.get_map()
        if mapping:
            # This copy prevents us from iterating over a view
            # while removing items from it, which is unsafe and
            # raises an exception with Python 3.
            for key in mapping.values():
                if key.fileobj == self:
                    continue
                assert isinstance(key.fileobj, SelectorsRequestHandler)
                handlers.append(key.fileobj)
        return handlers

    def __select(self, timeout=None):
        # type: (None | float) -> SelectorsEvents
        """Safer wrapper around select."""
        try:
            return self.selector.select(timeout)
        except socket.error as e:
            if not hasattr(e, "winerror") or e.winerror != 10038:
                raise
        # Operation attempted on something that is not a socket
        for handler in self.get_handlers():
            if handler.is_finished():
                self.shutdown_request(handler)
        return self.selector.select(timeout)

    def server_activate(self):
        # type: () -> None
        """Called by the constructor to activate the server."""
        super(SelectorsBaseServer, self).server_activate()  # calls listen()
        self.selector.register(self, selectors.EVENT_READ)

    def server_close(self):
        # type: () -> None
        """Called to clean up the server."""
        try:
            for handler in self.get_handlers():
                # noinspection PyBroadException
                try:
                    self.shutdown_request(handler)
                except Exception:
                    self.handle_error(handler)
                except:  # Fatal error  # noqa: E722
                    # If we can't gracefully shut down a client,
                    # let's exit early to avoid further issues and
                    # their performance cost.
                    raise
        finally:
            self.selector.close()
            super(SelectorsBaseServer, self).server_close()

    def get_request(self):  # type: ignore[override]
        # type: () -> tuple[SelectorsRequestHandler, ClientAddress]
        """Get a single TCP connection request.

        Compared to TCPServer's, a compatible handler is returned instead
        of a socket instance.
        """
        accepted_socket, address = super(SelectorsBaseServer,
                                         self).get_request()
        try:
            handler = self.handler_class(accepted_socket, address, self)
        except:  # noqa: E722
            # Prevent clients from hanging if we fail to create the handler
            accepted_socket.close()
            raise
        return handler, address

    def verify_request(self, request, client_address):  # type: ignore[override]  # noqa: E501
        # type: (SelectorsRequestHandler, ClientAddress) -> bool
        """Verify the request before processing it."""
        return True

    def process_request(self, handler, client_address):  # type: ignore[override]  # noqa: E501
        # type: (SelectorsRequestHandler, ClientAddress) -> None
        """Call finish_request.

        In Python's original implementation, this method was overridden
        by ForkingMixIn and ThreadingMixIn.
        """
        self.finish_request(handler, client_address)

    def finish_request(self, handler, client_address):  # type: ignore[override]  # noqa: E501
        # type: (SelectorsRequestHandler, ClientAddress) -> None
        """Called when the request handler creation is finished."""
        # FIXME: Is selector thread-safe?
        self.selector.register(handler, selectors.EVENT_READ)

    def shutdown_request(self, handler):  # type: ignore[override]
        # type: (SelectorsRequestHandler) -> None
        """Shutdown the request gracefully and close its file descriptor.

        MUST NOT RAISE EXCEPTIONS.
        """
        try:
            # Flush the socket
            handler.finish()
            # SHUT_WR should make future reads empty
            # SHUT_RD might raise exception on future reads
            handler.request.shutdown(socket.SHUT_WR)
        except socket.error:
            self.handle_error(handler)
        finally:
            self.close_request(handler)

    def close_request(self, handler):  # type: ignore[override]
        # type: (SelectorsRequestHandler) -> None
        """Close the request file descriptor.

        MUST NOT RAISE EXCEPTIONS.
        """
        try:
            # FIXME: Is selector thread-safe?
            self.selector.unregister(handler)
        except (KeyError, ValueError):
            # Might happen if an invalid handler/fd is provided.
            # Can sometimes occur when finish_request raises an exception.
            pass
        finally:
            handler.request.close()

    def serve_forever(self, poll_interval=0.5):
        # type: (float) -> None
        """Handle one request at a time until shutdown.

        Polls for shutdown every poll_interval seconds. Ignores
        self.timeout. If you need to do periodic tasks, do them in
        another thread.
        """
        self.__shutdown_request = False
        self.__is_shut_down.clear()
        try:
            while not self.__shutdown_request:
                events = self.__select(poll_interval)
                if self.__shutdown_request:
                    break
                self.__handle_events(events)
        finally:
            self.__shutdown_request = False
            self.__is_shut_down.set()

    def shutdown(self):
        # type: () -> None
        """Stops the serve_forever loop.

        Blocks until the loop has finished. This must be called while
        serve_forever() is running in another thread, or it will
        deadlock.
        """
        self.__shutdown_request = True
        self.__is_shut_down.wait()

    def is_shut_down(self):
        # type: () -> bool
        """Returns True if the server is shut down (gracefully or not)."""
        return self.__is_shut_down.is_set()

    def service_actions(self):
        # type: () -> None
        """Automatically called after requests handling.

        Called by serve_forever/handle_request via __handle_events.

        May be overridden by a subclass / Mixin to implement any code that
        needs to be run during the loop.

        MUST NOT RAISE EXCEPTIONS.
        """
        pass

    def handle_request(self, n=1):
        # type: (int) -> None
        """Handle at most `n` requests, possibly blocking.

        Respects self.timeout.
        """
        try:
            from time import monotonic as time  # Python 3 only
        except ImportError:
            from time import time

        # Support people who used socket.settimeout() to escape
        # handle_request before self.timeout was available.
        timeout = self.socket.gettimeout()
        if timeout is None:
            timeout = self.timeout
        elif self.timeout is not None:
            timeout = min(timeout, self.timeout)
        deadline = None if timeout is None else (time() + timeout)

        # Wait until a request arrives or the timeout expires - the loop is
        # necessary to accommodate early wakeups due to EINTR.
        while True:
            events = self.__select(timeout)
            if events:
                return self.__handle_events(events, n=n)
            if deadline is not None and time() >= deadline:
                return self.handle_timeout()

    def handle_error(self, handler=None, client_address=None):  # type: ignore[override]  # noqa: E501
        # type: (None | SelectorsRequestHandler, None | ClientAddress) -> None
        """Generic error handler, may be overridden.

        Some special cases:
         1. client_address is None: client's shutdown error
         2. handler is also None: server's accept error

        MUST NOT RAISE EXCEPTIONS.
        """
        active_exception = sys.exc_info()[1]
        if handler and active_exception is not None:
            handler.on_exception(active_exception)
        message = "Exception occurred during processing of {}".format(
            handler if handler else "accepting client"
        )
        if handler:
            message += " from {}".format(client_address) if client_address \
                 else " shutdown"
        separators = '-' * 40
        sys.stderr.write("{sep}\n{msg}\n{err}{sep}\n".format(
            sep=separators, msg=message, err=traceback.format_exc()
        ))
        sys.stderr.flush()


class SSLHandlerMixIn(object):
    """SSL MixIn class."""

    def get_ssl_context(self):
        # type: () -> ssl.SSLContext
        """Get SSL context, may be overridden."""
        return ssl.SSLContext(ssl.PROTOCOL_TLS)

    def __ssl_wrap_socket(self, sock):  # pyright: ignore
        # type: (socket.socket) -> socket.socket | ssl.SSLSocket
        """Wrap the socket if SSL is enabled."""
        if not self.ssl_cert or not self.ssl_key:
            return sock

        context = self.get_ssl_context()
        if self.ssl_ca:
            context.load_verify_locations(cafile=self.ssl_ca)

        context.load_cert_chain(self.ssl_cert, self.ssl_key)

        # Some Python versions might not enforce the timeout properly
        timeout = getattr(self, "timeout", None)  # type: None | float
        sock.settimeout(timeout)
        ssl_sock = context.wrap_socket(sock, server_side=True,
                                       do_handshake_on_connect=False)
        ssl_sock.settimeout(timeout)
        try:
            ssl_sock.do_handshake()
        except:  # noqa: E722
            ssl_sock.close()
            raise
        return ssl_sock

    # noinspection PyAttributeOutsideInit
    def setup(self):
        # type: () -> None
        """Load SSL options from server.kwargs if SSL is enabled."""
        assert isinstance(self, SelectorsRequestHandler)
        if hasattr(self.server, "kwargs"):
            assert isinstance(self.server, SelectorsBaseServer)
            kwargs = dict(self.server.kwargs)
            self.ssl_ca = kwargs.get("ssl_ca")  # type: None | str
            self.ssl_cert = kwargs.get("ssl_cert")  # type: None | str
            self.ssl_key = kwargs.get("ssl_key")  # type: None | str
            # noinspection PyUnresolvedReferences
            self.request = self.__ssl_wrap_socket(self.request)
        super(SSLHandlerMixIn, self).setup()


class WiiSSLHandlerMixIn(SSLHandlerMixIn):
    """SSL wrapper for network sockets aiming Wii compatibility.

    References:
    https://docs.python.org/2.7/library/ssl.html
    https://docs.python.org/3/library/ssl.html
    https://www.openssl.org/docs/man1.0.2/man1/ciphers.html
    https://www.openssl.org/docs/man1.1.1/man1/ciphers.html
    https://www.openssl.org/docs/man3.0/man1/openssl-ciphers.html
    """
    def get_ssl_context(self):
        # type: () -> ssl.SSLContext
        """Get a compatible Wii SSL context."""
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)

        if hasattr(ssl, "TLSVersion"):  # Since Python 3.7
            # Required since Python 3.10
            context.minimum_version = ssl.TLSVersion.SSLv3
        wii_ciphers = ":".join([
            "AES128-SHA", "AES256-SHA",
            # The following ones are often unavailable
            "DES-CBC-SHA", "3DES-CBC-SHA",
            "RC4-MD5", "RC4-SHA"
            # NB: Python might enforce additional (unsupported) ciphers
            # for security reasons
            # TODO: Disable them in Dolphin to emulate the Wii accurately
        ])

        # Try to enforce legacy ciphers/weak cert chain (OpenSSL >= 1.1 only)
        if ssl.OPENSSL_VERSION_INFO >= (1, 1):
            wii_ciphers += ":@SECLEVEL=0"

        context.set_ciphers(wii_ciphers)
        return context
