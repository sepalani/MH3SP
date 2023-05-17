#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2021-2022 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Utils helper module."""

import os
import logging
import socket

from collections import namedtuple
from functools import partial
from logging.handlers import TimedRotatingFileHandler
import traceback

try:
    # Python 3
    import configparser as ConfigParser
except ImportError:
    # Python 2
    import ConfigParser


CONFIG_FILE = "config.ini"
LOG_FOLDER = "logs"


class Logger(object):
    """Generic logging class."""

    def set_logger(self, logger):
        """Set logger."""
        self.logger = logger

    def debug(self, msg, *args, **kwargs):
        """Log a debug message."""
        if not hasattr(self, "logger"):
            return
        return self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """Log a message."""
        if not hasattr(self, "logger"):
            return
        return self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """Log a warning message."""
        if not hasattr(self, "logger"):
            return
        return self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """Log an error message."""
        if not hasattr(self, "logger"):
            return
        return self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
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
    """Python2/3 bytearray helper."""
    if isinstance(data, str):
        return bytearray((ord(c) for c in data))
    elif isinstance(data, bytearray):
        return data
    else:
        return bytearray(data)


def to_str(data):
    """Python2/3 str helper."""
    if isinstance(data, str):
        return data
    return "".join(chr(b) for b in to_bytearray(data))


def pad(s, size, p=b'\0'):
    data = bytearray(s + p * max(0, size-len(s)))
    data[-1] = 0
    return data


def hexdump(data):
    """Get data hexdump."""
    data = bytearray(data)
    line_format = "{line:08x} | {hex:47} | {ascii}"

    def hex_helper(b):
        return "{:02x}".format(b)

    def ascii_helper(b):
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


def get_config(name, config_file=CONFIG_FILE):
    """Get server config."""
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read(config_file)
    return {
        "IP": config.get(name, "IP"),
        "Port": config.getint(name, "Port"),
        "Name": config.get(name, "Name"),
        "MaxThread": config.getint(name, "MaxThread"),
        "UseSSL": config.getboolean(name, "UseSSL"),
        "LegacySSL": config.getboolean("SSL", "LegacySSL"),
        "SSLCert":
            config.get(name, "SSLCert") or
            config.get("SSL", "DefaultCert"),
        "SSLKey":
            config.get(name, "SSLKey") or
            config.get("SSL", "DefaultKey"),
        "LogFilename": config.get(name, "LogFilename"),
        "LogToConsole": config.getboolean(name, "LogToConsole"),
        "LogToFile": config.getboolean(name, "LogToFile"),
        "LogToWindow": config.getboolean(name, "LogToWindow"),
    }


def get_default_ip():
    """Get the default IP address"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def get_ip(ip):
    """Return the IP address that will be used."""
    return get_default_ip() if ip == "0.0.0.0" else ip


def argparse_from_config(config):
    """Argument parser from config."""
    import argparse

    def typebool(s):
        if isinstance(s, bool):
            return s
        s = s.lower()
        if s in ("on", "yes", "y", "true", "t", "1"):
            return True
        elif s in ("off", "no", "n", "false", "f", "0"):
            return False
        else:
            raise argparse.ArgumentTypeError("Boolean value expected.")

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--interactive", action="store_true",
                        dest="interactive",
                        help="create an interactive shell")
    parser.add_argument("-a", "--address", action="store", type=str,
                        default=config["IP"], dest="address",
                        help="set server address")
    parser.add_argument("-p", "--port", action="store", type=int,
                        default=config["Port"], dest="port",
                        help="set server port")
    parser.add_argument("-n", "--name", action="store", type=str,
                        default=config["Name"], dest="name",
                        help="set server name")
    parser.add_argument("-s", "--use-ssl", action="store", type=typebool,
                        default=config["UseSSL"], dest="use_ssl",
                        help="use SSL protocol")
    parser.add_argument("-f", "--legacy-ssl", action="store", type=typebool,
                        default=config["LegacySSL"], dest="legacy_ssl",
                        help="force legacy SSL ciphers")
    parser.add_argument("-c", "--ssl-cert", action="store", type=str,
                        default=config["SSLCert"], dest="ssl_cert",
                        help="set server SSL certificate")
    parser.add_argument("-k", "--ssl-key", action="store", type=str,
                        default=config["SSLKey"], dest="ssl_key",
                        help="set server SSL private key")
    parser.add_argument("-l", "--log-filename", action="store", type=str,
                        default=config["LogFilename"], dest="log_filename",
                        help="set server log filename")
    parser.add_argument("--log-to-file", action="store", type=typebool,
                        default=config["LogToFile"], dest="log_to_file",
                        help="log output to file")
    parser.add_argument("--log-to-console", action="store", type=typebool,
                        default=config["LogToConsole"], dest="log_to_console",
                        help="log output to console")
    parser.add_argument("--log-to-window", action="store", type=typebool,
                        default=config["LogToWindow"], dest="log_to_window",
                        help="log output to a new window")
    return parser


def create_server(server_class, server_handler,
                  address="0.0.0.0", port=8200, name="Server", max_thread=0,
                  use_ssl=True, ssl_cert="server.crt", ssl_key="server.key",
                  log_to_file=True, log_filename="server.log",
                  log_to_console=True, log_to_window=False, legacy_ssl=False,
                  debug_mode=False):
    """Create a server, its logger and the SSL context if needed."""
    logger = create_logger(
        name, level=logging.DEBUG if debug_mode else logging.INFO,
        log_to_file=log_filename if log_to_file else "",
        log_to_console=log_to_console,
        log_to_window=log_to_window)
    server = server_class((address, port), server_handler, max_thread, logger,
                          debug_mode)

    if use_ssl:
        import ssl

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
        if legacy_ssl:
            # https://www.openssl.org/docs/man1.0.2/man1/ciphers.html
            # https://www.openssl.org/docs/man1.1.1/man1/ciphers.html
            # https://www.openssl.org/docs/man3.0/man1/openssl-ciphers.html
            openssl_version = ssl.OPENSSL_VERSION_INFO[:2]
            message = "Unsupported LegacySSL option (OpenSSL {}.{})".format(
                *openssl_version)
            assert openssl_version > (1, 0), message
            wii_ciphers += ":@SECLEVEL=0"  # Allow weak cert chain
        context.set_ciphers(wii_ciphers)
        context.load_cert_chain(ssl_cert, ssl_key)
        server.socket = context.wrap_socket(server.socket, server_side=True)

    return server


server_base = namedtuple("ServerBase", ["name", "cls", "handler"])


def create_server_from_base(name, server_class, server_handler, silent=False,
                            debug_mode=False):
    """Create a server based on its config parameters."""
    config = get_config(name)
    return create_server(
        server_class, server_handler,
        address=config["IP"],
        port=config["Port"],
        name=config["Name"],
        max_thread=config["MaxThread"],
        use_ssl=config["UseSSL"],
        legacy_ssl=config["LegacySSL"],
        ssl_cert=config["SSLCert"],
        ssl_key=config["SSLKey"],
        log_to_file=config["LogToFile"],
        log_filename=config["LogFilename"],
        log_to_console=config["LogToConsole"] and not silent,
        log_to_window=config["LogToWindow"],
        debug_mode=debug_mode
    ), config["LogToWindow"]


def server_main(name, server_class, server_handler):
    """Create a server main based on its config parameters."""
    config = get_config(name)
    parser = argparse_from_config(config)
    args = parser.parse_args()
    server = create_server(server_class, server_handler, **{
        k: v for k, v in vars(args).items()
        if k not in ("interactive",)
    })

    try:
        import threading

        thread = threading.Thread(target=server.serve_forever)
        thread.start()

        if args.interactive:
            import code
            code.interact(local=locals())  # Block until the interpreter exited

        if args.log_to_window:
            from other.ui import update as ui_update

        while thread.is_alive():
            thread.join(0.1)  # Timeout allows main thread to handle signals
            if args.log_to_window:
                ui_update()
    except KeyboardInterrupt:
        server.info("Interrupt key was pressed, closing server...")
    except Exception:
        server.error('Unexpected exception caught...')
        traceback.print_exc()
    finally:
        server.close()
