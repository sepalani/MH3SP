#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2022-2025 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Monster Hunter PAT Server module."""

import multiprocessing
import random
import sys
import threading
import traceback

from mh.time_utils import Timer
from other.net_utils import \
    PacketHandler, WiiSSLHandlerMixIn, SelectorsBaseServer
from other.python import PYTHON_VERSION, TYPE_CHECKING
from other.utils import Logger

if TYPE_CHECKING or PYTHON_VERSION == 3:
    import queue
    import selectors
else:
    import Queue as queue
    import externals.selectors2 as selectors

if TYPE_CHECKING:
    from typing import Any

    # noinspection PyCompatibility
    PacketQueue = queue.Queue[
        tuple["BasicPatHandler", Any, int]
        | tuple[None, None, None]
    ]
else:
    PacketQueue = queue.Queue


class BasicPatHandler(WiiSSLHandlerMixIn, PacketHandler):  # type: ignore[misc]
    """Dummy queueable PAT packet handler class."""

    # Prevents indefinite recv from invalid headers
    timeout = 2.0

    # noinspection PyAttributeOutsideInit
    def setup(self):
        # type: () -> None
        """Prepare the handler and its default properties."""
        self.worker_index = 0
        return super(BasicPatHandler, self).setup()

    def handle_packet(self, seq, packet_id, data):  # type: ignore[override]
        # type: (int, int, bytes) -> None
        """Add the received packet to the server's queue."""
        assert isinstance(self.server, BasicPatServer)
        self.server.queue_work(self, (packet_id, data, seq),
                               selectors.EVENT_READ)

    def send_packet(self, packet_id, data, seq):  # type: ignore[override]
        # type: (int, bytes, int) -> None
        """Change parameters order to match the generic one."""
        return super(BasicPatHandler, self).send_packet(seq, packet_id, data)

    def on_packet(self, packet_id, data, seq):
        # type: (int, bytes, int) -> None
        """Called when there is a packet to be handled

        This method would be called from a worker thread (Not Thread Safe)
        """
        pass


class BasicPatServer(SelectorsBaseServer, Logger):
    """Basic PAT packet server with worker threads."""

    # noinspection PyAttributeOutsideInit
    def server_activate(self):
        # type: () -> None
        """Set the server default properties."""
        self._random = random.SystemRandom()
        self.write_watch = Timer()
        self.write_timeout = 1  # Seconds
        self.worker_threads = []  # type: list[threading.Thread]
        self.worker_queues = []  # type: list[PacketQueue]
        self.max_thread = \
            self.kwargs.get("max_thread") or multiprocessing.cpu_count()
        return super(BasicPatServer, self).server_activate()

    # noinspection PyBroadException
    def _worker_target(self, work_queue):
        # type: (PacketQueue) -> None
        """Worker thread main loop to handle a PacketQueue."""
        try:
            while not self.is_shut_down():
                try:
                    handler, packet, event = work_queue.get(block=True)
                except queue.Empty:
                    continue

                if self.is_shut_down() or handler is None or \
                        packet is None:  # extra check for type checkers
                    break  # shutting down

                if handler.is_finished():
                    continue

                assert event == selectors.EVENT_READ

                try:
                    try:
                        handler.on_packet(*packet)
                    except Exception as e:
                        handler.on_exception(e)

                    if handler.is_finished():
                        self.shutdown_request(handler)
                except:  # noqa: E722
                    self.error(
                        "Worker failure with %s:\n%s", handler,
                        traceback.format_exc().rstrip('\n')
                    )
                    raise
        finally:
            self.info("Worker(%s) exiting...",
                      threading.current_thread().name)

    def queue_work(self, handler, work_data, event):
        # type: (BasicPatHandler, Any, int) -> None
        """Add a packet to the handler's PacketQueue."""
        if handler.is_finished():
            return

        thread_queue = self.worker_queues[handler.worker_index]
        thread_queue.put((handler, work_data, event), block=True)

    def initialize_workers(self):
        # type: () -> None
        """Initialize workers queues/threads."""
        for n in range(self.max_thread):
            thread_queue = PacketQueue()
            thread = threading.Thread(
                target=self._worker_target,
                args=(thread_queue,),
                name="{}.Worker-{}".format(self.__class__.__name__, n)
            )
            self.worker_queues.append(thread_queue)
            self.worker_threads.append(thread)
            thread.start()

    def finish_request(self, handler, client_address):  # type: ignore[override]  # noqa: E501
        # type: (BasicPatHandler, tuple[str, int]) -> None
        """Finish the request handler construction."""
        handler.worker_index = self._random.randint(0,
                                                    len(self.worker_queues)-1)
        return super(BasicPatServer, self).finish_request(handler,
                                                          client_address)

    def serve_forever(self, poll_interval=0.5):
        # type: (float) -> None
        """Start the worker threads and the server main loop."""
        self.initialize_workers()
        return super(BasicPatServer, self).serve_forever(poll_interval)

    # noinspection PyBroadException
    def service_actions(self):
        # type: () -> None
        """Called on each server loop.

        Alternative to monitor write events which is CPU intensive.

        Reminder: MUST NOT RAISE EXCEPTIONS.
        """
        if self.write_watch.elapsed() >= self.write_timeout:
            try:
                for handler in self.get_handlers():
                    assert isinstance(handler, BasicPatHandler)

                    try:
                        handler.on_send()
                    except Exception as e:
                        handler.on_exception(e)

                    if handler.is_finished():
                        self.shutdown_request(handler)
            except Exception:
                self.error("%s", traceback.format_exc().rstrip('\n'))
            finally:
                self.write_watch.restart()
        return super(BasicPatServer, self).service_actions()

    def server_close(self):
        # type: () -> None
        """Clean up the server and its worker threads."""
        try:
            super(BasicPatServer, self).server_close()
        finally:
            if not hasattr(self, "worker_queues"):
                return  # Server startup interrupted (bind error?)

            for q in self.worker_queues:
                q.put((None, None, None), block=True)

            for t in self.worker_threads:
                if t.is_alive():
                    t.join()

            self.worker_queues = []
            self.worker_threads = []

            self.info('Server closed')

    def handle_error(self, handler=None, client_address=None):  # type: ignore[override]  # noqa: E501
        # type: (None | BasicPatHandler, None | tuple[str, int]) -> None
        """Custom error handler to use server's logger.

        MUST NOT RAISE EXCEPTIONS.
        """
        active_exception = sys.exc_info()[1]
        # Handle client related exceptions
        if handler and active_exception is not None:
            handler.on_exception(active_exception)
            return
        # Handle server related exceptions
        message = "Exception occurred during processing of {}".format(
            handler if handler else "accepting client"
        )
        if handler:
            message += " from {}".format(client_address) if client_address \
                 else " shutdown"
        self.error("%s\n%s", message, traceback.format_exc().rstrip('\n'))
