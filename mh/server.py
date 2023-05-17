#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2022-2023 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Monster Hunter PAT Server module."""

import multiprocessing
import random
import socket
import struct
import threading

from mh.time_utils import Timer

try:
    # Python 3
    import queue
    import selectors
except ImportError:
    # Python 2
    import Queue as queue
    import externals.selectors2 as selectors


try:
    from typing import List, Tuple
except ImportError:
    pass


class BasicPatHandler(object):
    def __init__(self, socket, client_address, server):
        # type: (socket.socket, Tuple[str, int], BasicPatServer)  -> None
        self.socket = socket
        self.client_address = client_address
        self.server = server
        self.finished = False
        self.rw = threading.Lock()
        self.setup()

    def fileno(self):
        # type: () -> int
        return self.socket.fileno()

    def setup(self):
        self.rfile = self.socket.makefile('rb', -1)
        self.wfile = self.socket.makefile('wb', 0)

        self.on_init()

    def on_init(self):
        """Called after setup"""
        pass

    def on_exception(self, e):
        # type: (Exception) -> None
        """Called when during recv/write an exception ocurred"""
        pass

    def on_recv(self):
        """Called when the socket have bytes to be readed

        ** This method would be called by the server thread

        """
        header = self.rfile.read(8)
        if not len(header):
            # The socket was closed by externally
            return None

        if len(header) < 8:
            # Invalid packet header
            return None

        return self.recv_packet(header)

    def on_packet(self, data):
        """ Called when there is a packet to be handled

        ** This method would be called from a worker thread (Not Thread Safe)

        """

    def recv_packet(self, header):
        """Receive PAT packet."""
        size, seq, packet_id = struct.unpack(">HHI", header)
        data = self.rfile.read(size)
        return packet_id, data, seq

    def send_packet(self, packet_id=0, data=b'', seq=0):
        """Send PAT packet."""
        self.wfile.write(struct.pack(
            ">HHI",
            len(data), seq, packet_id
        ))
        if data:
            self.wfile.write(data)

    def on_tick(self):
        """Called every time the server tick

        ** Currently executed from the server thread

        """
        pass

    def on_finish(self):
        """Called before finish"""
        pass

    def is_finished(self):
        return self.finished

    def finish(self):
        """Called when the handler is being disposed"""

        if self.finished:
            return

        try:
            self.on_finish()
        except Exception as e:
            pass

        self.finished = True

        try:
            self.wfile.close()
        except Exception:
            pass

        try:
            self.rfile.close()
        except Exception:
            pass


class BasicPatServer(object):

    socket_queue_size = 5

    address_family = socket.AF_INET

    socket_type = socket.SOCK_STREAM

    def __init__(self, server_address, RequestHandlerClass, max_threads,
                 bind_and_activate=True):
        # type: (Tuple[str, int], BasicPatHandler, int, bool) -> None
        """Constructor.  May be extended, do not override."""
        self.server_address = server_address
        self.RequestHandlerClass = RequestHandlerClass
        self.__is_shut_down = threading.Event()
        self.__shutdown_request = False
        self.socket = socket.socket(self.address_family, self.socket_type)
        self._random = random.SystemRandom()  # type: random.SystemRandom
        self.handlers = []  # type: List[BasicPatHandler]
        self.worker_threads = []  # type: List[threading.Thread]
        self.worker_queues = []  # type: list[queue.queue]
        self.selector = selectors.DefaultSelector()

        if max_threads <= 0:
            max_threads = multiprocessing.cpu_count()

        for _ in range(max_threads):
            thread_queue = queue.Queue()
            thread = threading.Thread(target=self._worker_target,
                                      args=(thread_queue,))
            self.worker_queues.append(thread_queue)
            self.worker_threads.append(thread)
            thread.start()

        if bind_and_activate:
            try:
                self.server_bind()
                self.server_activate()
            except Exception:
                self.close()
                raise

    def server_bind(self):
        self.socket.bind(self.server_address)
        self.server_address = self.socket.getsockname()

    def server_activate(self):
        self.socket.listen(0)

    def fileno(self):
        """Return server socket file descriptor.

        Interface required by selector.

        """
        return self.socket.fileno()

    def serve_forever(self):
        self.__is_shut_down.clear()
        try:
            with self.selector as selector:
                selector.register(self, selectors.EVENT_READ)

                write_watch = Timer()
                write_timeout = 1  # Seconds
                while not self.__shutdown_request:
                    ready = selector.select(write_timeout)
                    if self.__shutdown_request:
                        break

                    for (key, event) in ready:
                        selected = key.fileobj
                        if selected == self:
                            self.accept_new_connection()
                        else:
                            assert event == selectors.EVENT_READ
                            try:
                                packet = selected.on_recv()
                                if packet is None:
                                    if selected.is_finished():
                                        self.remove_handler(selected)
                                    continue

                                self._queue_work(selected, packet, event)
                            except Exception as e:
                                selected.on_exception(e)
                                if selected.is_finished():
                                    self.remove_handler(selected)
                    if write_watch.elapsed() >= write_timeout:
                        try:
                            for handler in self.handlers:
                                try:
                                    handler.on_tick()
                                except Exception as e:
                                    handler.on_exception(e)

                                if handler.is_finished():
                                    self.remove_handler(handler)
                        finally:
                            write_watch.restart()
        finally:
            self.__is_shut_down.set()

    def _worker_target(self, work_queue):
        # type: (queue.Queue) -> None

        while not self.__shutdown_request:
            try:
                handler, packet, event = work_queue.get(block=True)
            except queue.Empty:
                continue

            if self.__shutdown_request:
                break

            if handler.is_finished():
                continue

            assert event == selectors.EVENT_READ

            try:
                handler.on_packet(packet)
            except Exception as e:
                handler.on_exception(e)

            if handler.is_finished():
                self.remove_handler(handler)

    def accept_new_connection(self):
        # type: () -> None

        try:
            client_socket, client_address = self.socket.accept()
        except Exception as e:
            self.error('Error accepting connection (1). {}'.format(e))
            return

        try:
            handler = self.RequestHandlerClass(client_socket, client_address,
                                               self)
        except Exception:
            self.error('Error accepting connection (2). {}'.format(e))
            return

        handler.__worker_thread = \
            self._random.randint(0, len(self.worker_queues)-1)

        self.selector.register(handler, selectors.EVENT_READ)
        self.handlers.append(handler)

    def _queue_work(self, handler, work_data, event):
        # type: (BasicPatHandler, any, int) -> None
        if handler.is_finished():
            return

        thread_queue = self.worker_queues[handler.__worker_thread]
        thread_queue.put((handler, work_data, event), block=True)

    def remove_handler(self, handler):
        # type: (BasicPatHandler) -> None
        try:
            self.handlers.remove(handler)
        except Exception:
            pass

        try:
            self.selector.unregister(handler)
        except Exception:
            pass

        try:
            handler.finish()
        except Exception:
            pass

        try:
            handler.socket.close()
        except Exception:
            pass

    def close(self):
        """Called to clean-up the server.

        May be overridden.

        """
        self.__shutdown_request = True
        self.socket.close()
        self.__is_shut_down.wait()

        for h in self.handlers:
            try:
                h.finish()
            except Exception:
                pass

        for q in self.worker_queues:
            q.put((None, None, None), block=True)

        for t in self.worker_threads:
            t.join()

        self.worker_queues = []
        self.selector = None
        self.worker_threads = []
        self.__shutdown_request = False
        self.info('Server Closed')
