#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2021-2025 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Utils helper module."""

import os
import logging
import socket
import sys
import traceback

from collections import namedtuple
from functools import partial
from logging.handlers import TimedRotatingFileHandler
from other.config import config_from_name
from other.debug import register_debug_signal, dry_run
from other.python import PYTHON_VERSION, TYPE_CHECKING

if TYPE_CHECKING or PYTHON_VERSION == 3:
    basestring = str  # Python 2: str, unicode
if TYPE_CHECKING:
    from argparse import Namespace  # noqa: F401
    from collections.abc import Sequence  # noqa: F401
    from typing import Any, NamedTuple  # noqa: F401

    from mh.pat import PatServer, PatRequestHandler


LOG_FOLDER = "logs"


class Logger(object):
    """Generic logging class."""

    def set_logger(self, logger):
        # type: (Logger) -> None
        """Set logger."""
        self.logger = logger

    def debug(self, msg, *args, **kwargs):
        # type: (str, *Any, **Any) -> None
        """Log a debug message."""
        if not hasattr(self, "logger"):
            return
        return self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        # type: (str, *Any, **Any) -> None
        """Log a message."""
        if not hasattr(self, "logger"):
            return
        return self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        # type: (str, *Any, **Any) -> None
        """Log a warning message."""
        if not hasattr(self, "logger"):
            return
        return self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        # type: (str, *Any, **Any) -> None
        """Log an error message."""
        if not hasattr(self, "logger"):
            return
        return self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        # type: (str, *Any, **Any) -> None
        """Log a critical message."""
        if not hasattr(self, "logger"):
            return
        return self.logger.critical(msg, *args, **kwargs)


class GenericUnpacker(object):
    """Generic unpacker that maps unpack and pack functions.

    This class streamlines the unpacking process by keeping track of the
    data and its current offset on top of checking the (un)packing functions
    accuracy.
    """
    MAPPING = dict()

    def __init__(self, data, offset=0, check=True):
        self.data = data
        self.offset = offset
        self.check = check
        for name, (unpack_function, pack_function) in self.MAPPING.items():
            self.bind(name, unpack_function, pack_function)

    def __len__(self):
        """Used for truth value testing instead of __nonzero__ and __bool__.

        References:
        https://docs.python.org/2/reference/datamodel.html#object.__nonzero__
        https://docs.python.org/3/reference/datamodel.html#object.__bool__
        """
        return len(self.data[self.offset:])

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_val, tb):
        if ex_type or ex_val or tb:
            return  # Raise an exception normally
        if self.check and self:
            message = (
                "Data buffer not emptied, remaining bytes at offset {}:\n"
                " -> {!r}"
            ).format(self.offset, self.data[self.offset:])
            raise AssertionError(message)

    def bind(self, name, unpack_function, pack_function):
        def handler(self, name, unpack_function, pack_function,
                    *args, **kwargs):
            unpack_args = args + (self.data, self.offset)
            unpack_result = unpack_function(*unpack_args, **kwargs)

            if isinstance(unpack_result, tuple):
                pack_args = args + unpack_result
            else:
                pack_args = args + (unpack_result,)
            pack_result = pack_function(*pack_args, **kwargs)

            length = len(pack_result)
            matching_results = self.data[self.offset:
                                         self.offset+length] == pack_result
            message = "Unpacker mismatch in {}:\n{!r}\n{!r}".format(
                name, self.data[self.offset:self.offset+length], pack_result
            )
            assert matching_results, message
            self.offset += len(pack_result)
            return unpack_result

        setattr(self, name,
                partial(handler, self, name, unpack_function, pack_function))


def to_bytearray(data):
    # type: (Any) -> bytearray
    """Python2/3 bytearray helper."""
    if isinstance(data, basestring):
        return bytearray((ord(c) % 256 for c in data))
    elif isinstance(data, bytearray):
        return data
    else:
        return bytearray(data)


def to_bytes(data):
    # type: (Any) -> bytes
    return bytes(to_bytearray(data))


def to_str(data):
    # type: (Any) -> str
    """Python2/3 str helper."""
    if isinstance(data, str):
        return data
    return "".join(chr(b) for b in to_bytearray(data))


def pad(s, size, p=b'\0'):
    # type: (bytes, int, bytes) -> bytearray
    data = bytearray(s + p * max(0, size-len(s)))
    data[-1] = 0
    return data


def hexdump(data):
    # type: (bytes | bytearray) -> str
    """Get data hexdump."""
    data = bytearray(data)
    line_format = "{line:08x} | {hex:47} | {ascii}"

    def hex_helper(b):
        # type: (int) -> str
        return "{:02x}".format(b)

    def ascii_helper(b):
        # type: (int) -> str
        return chr(b) if 0x20 <= b < 0x7F else '.'

    return "\n".join(
        line_format.format(
            line=i,
            hex=" ".join(hex_helper(b) for b in data[i:i+16]),
            ascii="".join(ascii_helper(b) for b in data[i:i+16])
        )
        for i in range(0, len(data), 16)
    )


def create_logger(name, level=logging.DEBUG, log_to_file="",
                  log_to_console=False, log_to_window=False):
    # type: (str, int, str, bool, bool) -> logging.Logger
    """Create a logger."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logging_formatter = logging.Formatter(
        "[%(asctime)s | {}] %(message)s".format(name),
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    if log_to_console:
        console_logger = logging.StreamHandler()
        console_logger.setFormatter(logging_formatter)
        logger.addHandler(console_logger)

    if log_to_file:
        if not os.path.exists(LOG_FOLDER):
            os.makedirs(LOG_FOLDER)
        filename = os.path.join(LOG_FOLDER, log_to_file)

        file_logger = TimedRotatingFileHandler(
            filename, when='midnight', backupCount=10
        )
        file_logger.setFormatter(logging_formatter)
        logger.addHandler(file_logger)

    if log_to_window:
        from other.ui import LoggerTk

        window = LoggerTk()
        window.title(name)
        window.get_handler().setFormatter(logging_formatter)
        window.set_logger(logger)

    return logger


def get_default_ip():
    # type: () -> str
    """Get the default IP address"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]  # type: str
    s.close()
    return ip


def get_ip(ip):
    # type: (str) -> str
    """Return the IP address that will be used."""
    return get_default_ip() if ip == "0.0.0.0" else ip


def get_external_ip(config):
    # type: (dict[str, Any]) -> str
    """Return the IP address advertised by the server.

    It's useful when the public IP address can't easily be retrieved.
    For instance, when behind a NAT or some cloud infrastructures.
    """
    return config["ExternalIP"] or get_ip(config["IP"])


def create_server(server_class, server_handler,
                  address="0.0.0.0", port=8200, name="Server", max_thread=0,
                  use_ssl=True, ssl_cert="server.crt", ssl_key="server.key",
                  log_to_file=True, log_filename="server.log",
                  log_to_console=True, log_to_window=False,
                  debug_mode=False, no_timeout=False, **kwargs):
    # type: (type[PatServer], type[PatRequestHandler], str, int, str, int, bool, str | None, str | None, bool, str, bool, bool, bool, bool, **Any) -> PatServer  # noqa: E501
    """Create a server, its logger and the SSL context if needed."""
    logger = create_logger(
        name, level=logging.DEBUG if debug_mode else logging.INFO,
        log_to_file=log_filename if log_to_file else "",
        log_to_console=log_to_console,
        log_to_window=log_to_window)
    if not use_ssl:
        ssl_cert = None
        ssl_key = None
    return server_class(
        (address, port), server_handler,
        max_thread=max_thread, logger=logger, debug_mode=debug_mode,
        ssl_cert=ssl_cert, ssl_key=ssl_key, no_timeout=no_timeout,
        **kwargs
    )


if TYPE_CHECKING:
    # Python 2 doesn't support the class syntax
    server_base = NamedTuple("server_base", [
        ("name", str),
        ("cls", type[PatServer]),
        ("handler", type[PatRequestHandler])
    ])
else:
    server_base = namedtuple("ServerBase", ["name", "cls", "handler"])


def create_server_from_base(name, server_class, server_handler, cmd_args=None):
    # type: (str, type[PatServer], type[PatRequestHandler], Sequence[str] | None) -> tuple[PatServer, Namespace] | tuple[None, None]  # noqa: E501
    """Create a server based on its config parameters and supplied args.

    If args is None, sys.argv is used (see ArgumentParser.parser_args).
    """
    config = config_from_name(name)
    if not config["Enabled"]:
        return None, None
    # TODO: Backport central config code if needed
    parser = config.to_argument_parser()
    args = parser.parse_args(cmd_args)
    kwargs = {
        k: v for k, v in vars(args).items()
        if k not in ("interactive", "dry_run")
    }
    return create_server(server_class, server_handler, **kwargs), args


def server_main(name, server_class, server_handler):
    # type: (str, type[PatServer], type[PatRequestHandler]) -> None
    """Create a server main based on its config parameters."""
    register_debug_signal()

    server, args = create_server_from_base(name, server_class,
                                           server_handler)
    assert server and args, "Server disabled by the config file"

    try:
        import threading

        thread = threading.Thread(target=server.serve_forever)
        thread.start()

        if args.dry_run:
            dry_run()

        if args.interactive:
            import code
            code.interact(local=locals())  # Block until the interpreter exited

        if args.log_to_window:
            from other.ui import update as ui_update
        else:
            def ui_update():
                pass

        while thread.is_alive():
            thread.join(0.1)  # Timeout allows main thread to handle signals
            ui_update()
    except KeyboardInterrupt:
        server.info("Interrupt key was pressed, closing server...")
    except Exception:
        server.error('Unexpected exception caught...')
        traceback.print_exc()
        sys.exit(1)
    finally:
        server.shutdown()
        server.server_close()
