#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2021-2025 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Config module."""

from collections import OrderedDict

from other.python import PYTHON_VERSION, TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable  # noqa: F401
    from typing import Any
    OrderedDictT = OrderedDict[str, Any]
    from configparser import RawConfigParser
    from argparse import ArgumentParser  # noqa: F401
else:  # workaround to avoid some type hinting issues
    OrderedDictT = OrderedDict
    if PYTHON_VERSION == 2:
        from ConfigParser import RawConfigParser
    else:
        from configparser import RawConfigParser


CONFIG_FILE = "config.ini"


class ConfigLoader(RawConfigParser):
    """Generic INI config loader class."""
    def __init__(self, config_path):
        # type: (str) -> None
        RawConfigParser.__init__(self, allow_no_value=True)
        # Override this member to avoid options being lowercased
        self.optionxform = lambda optionstr: str(optionstr)
        self.read(config_path)
        self._config_path = config_path

    def reload(self):
        # type: () -> None
        self.read(self._config_path)


class ConfigSection(OrderedDictT):
    """ConfigSection helper class.

    This class loads all options from a config section into a dict.
    """
    BOOL = tuple()  # type: tuple[str, ...]
    INT = tuple()  # type: tuple[str, ...]
    FLOAT = tuple()  # type: tuple[str, ...]
    STR = tuple()  # type: tuple[str, ...]
    # Special cases
    SP = {}  # type: dict[str, Callable[[ConfigLoader, str], str]]

    def __init__(self, section_name, config_path=CONFIG_FILE):
        # type: (str, str) -> None
        super(ConfigSection, self).__init__()
        self._config = ConfigLoader(config_path)
        self._section_name = section_name
        self._config_path = config_path
        self._load_section()
        self._validate()

    def _load_section(self):
        # type: () -> None
        for option in self._config.options(self._section_name):
            self[option] = (
                self._config.getboolean(self._section_name, option)
                if option in self.BOOL
                else
                self._config.getint(self._section_name, option)
                if option in self.INT
                else
                self._config.getfloat(self._section_name, option)
                if option in self.FLOAT
                else
                self.SP[option](self._config, self._section_name)
                if option in self.SP
                else
                self._config.get(self._section_name, option)
            )

    def _validate(self):
        # type: () -> None
        missing_options = []  # type: list[str]
        for typed_options in (self.BOOL, self.INT, self.FLOAT, self.STR):
            missing_options.extend(
                option
                for option in typed_options
                if option not in self
            )
        missing_options.extend(
            option
            for option in self.SP
            if option not in self
        )
        message = '{}: section "{}" has missing option(s): {}'.format(
            self._config_path, self._section_name, ", ".join(missing_options)
        )
        assert not missing_options, message

    def reload(self):
        # type: () -> None
        """Reload the config."""
        self._config.reload()
        self._load_section()
        self._validate()


class BaseServerConfig(ConfigSection):
    SERVER_NAMES = tuple()  # type: tuple[str, ...]
    INT = ("Port",)
    BOOL = ("UseSSL", "LogToConsole", "LogToFile", "LogToWindow", "Enabled")
    STR = ("IP", "ExternalIP", "Name", "LogFilename")
    SP = {
        "SSLCert":
            lambda cfg, section: cfg.get(section, "SSLCert")
            or cfg.get("SSL", "DefaultCert"),
        "SSLKey":
            lambda cfg, section: cfg.get(section, "SSLKey")
            or cfg.get("SSL", "DefaultKey")
    }

    def to_argument_parser(self):
        # type: () -> ArgumentParser
        """Create a generic ArgumentParser from the server config.

        It can be used in a main function to parse command-line arguments."""
        # TODO: Move the code here when the refactoring is completed
        return argparse_from_config(self)


class ServerConfig(BaseServerConfig):
    """OPN/LMP/FMP/RFP server config."""
    SERVER_NAMES = ("OPN", "LMP", "FMP", "RFP")
    INT = BaseServerConfig.INT + ("MaxThread",)


class MySQLConfig(ConfigSection):
    BOOL = ("enabled",)
    STR = ("user", "password", "host", "database",
           "ssl_ca", "ssl_cert", "ssl_key")

    def __init__(self, section_name="MYSQL", config_path=CONFIG_FILE):
        # type: (str, str) -> None
        super(MySQLConfig, self).__init__(section_name, config_path)

    def is_enabled(self):
        # type: () -> bool
        return self["enabled"]  # type: ignore

    def connect_kwargs(self):
        # type: () -> dict[str, Any]
        from mysql.connector.constants import ClientFlag
        kwargs = {
            k: v for k, v in self.items()
            if k not in ("enabled",)
        }  # type: dict[str, Any]
        kwargs.update({
            "charset": "utf8",
            "autocommit": True,
            "client_flags": [ClientFlag.SSL] if kwargs["ssl_ca"] else None,
            "ssl_ca": kwargs["ssl_ca"] or None,
            "ssl_cert": kwargs["ssl_cert"] or None,
            "ssl_key": kwargs["ssl_key"] or None
        })
        return kwargs


# TODO: Backport latest_patch and central config code


def config_from_name(name):
    # type: (str) -> ServerConfig | CentralConfig
    """Return the server config based on its name."""
    if name in ServerConfig.SERVER_NAMES:
        return ServerConfig(name)
    else:
        raise NotImplementedError()


def argparse_from_config(config):
    # type: (BaseServerConfig) -> ArgumentParser
    """Argument parser from config."""
    import argparse

    def typebool(s):
        # type: (bool | str) -> bool
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
    parser.add_argument("-d", "--debug_mode", action="store_true",
                        dest="debug_mode",
                        help="enable debug mode, disabling timeouts and \
                        lower logging verbosity level")
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
    parser.add_argument("--dry-run", action="store_true",
                        dest="dry_run",
                        help="dry run to test the server")
    parser.add_argument("-t", "--no-timeout", action="store_true",
                        dest="no_timeout",
                        help="disable player timeouts")
    if "MaxThread" in config:
        parser.add_argument("--max-thread", action="store", type=int,
                            default=config["MaxThread"], dest="max_thread",
                            help="log output to a new window")
    return parser
