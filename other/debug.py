#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2023-2024 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Debugging helper module.

 - Python 2.7 debugging (VS Code)
https://stackoverflow.com/questions/72214043/how-to-debug-python-2-7-code-with-vs-code

 - Python 2.7 debugging (Visual Studio)
Debug > Attach to Process... > Python remote (debugpy)

 - Debuggers
https://wiki.python.org/moin/PythonDebuggingTools
"""

import traceback
import signal

from other.python import PYTHON_VERSION, TYPE_CHECKING

if TYPE_CHECKING or PYTHON_VERSION == 3:
    from configparser import RawConfigParser
else:
    from ConfigParser import RawConfigParser

if TYPE_CHECKING:
    from collections.abc import Callable  # noqa: F401
    from types import FrameType  # noqa: F401
    from typing import Any  # noqa: F401

DEBUG_INI_PATH = "debug.ini"


def debugpy_handler(sig, frame, addr="127.0.0.1", port="5678", **kwargs):
    # type: (int, FrameType, str, str, **Any) -> None
    """Handler for debugpy on Visual Studio and VS Code.

    References:
    https://github.com/microsoft/debugpy/
    https://code.visualstudio.com/docs/python/debugging
    https://learn.microsoft.com/visualstudio/python/debugging-python-in-visual-studio
    """
    import debugpy  # type: ignore
    s = (addr, int(port))  # config's items are str
    debugpy.listen(s)
    print("Waiting for client on {}:{}\n".format(*s))
    debugpy.wait_for_client()


def trepan_handler(sig, frame, **kwargs):
    # type: (int, FrameType, **Any) -> None
    """Handler for trepan2/trepan3k.

    References:
    https://github.com/rocky/python2-trepan/
    https://github.com/rocky/python3-trepan/
    https://python2-trepan.readthedocs.io/en/latest/entry-exit.html
    """
    from trepan.api import debug  # type: ignore
    debug()


def pudb_handler(sig, frame, **kwargs):
    # type: (int, FrameType, **Any) -> None
    """Handler for pudb on Linux and Cygwin.

    References:
    https://github.com/inducer/pudb
    https://documen.tician.de/pudb/
    """
    import pudb  # type: ignore
    pudb.set_trace()


def breakpoint_handler(sig, frame, **kwargs):
    # type: (int, FrameType, **Any) -> None
    """PDB/breakpoint handler.

    References:
    https://peps.python.org/pep-0553/
    https://realpython.com/python-debugging-pdb/
    """
    try:
        breakpoint()  # Python >= 3.7
    except NameError:
        import pdb
        pdb.set_trace()


def code_interact_handler(sig, frame, **kwargs):
    # type: (int, FrameType, **Any) -> None
    """Python interpreter handler.

    References:
    https://docs.python.org/2.7/library/code.html
    https://docs.python.org/3/library/code.html
    """
    import code
    local = {"_frame": frame}
    local.update(frame.f_globals)
    local.update(frame.f_locals)
    code.interact(local=local)


DEBUG_HANDLERS = {
    "DEBUGPY": debugpy_handler,
    "TREPAN": trepan_handler,
    "PUDB": pudb_handler,
    "BREAKPOINT": breakpoint_handler,
    "CODE": code_interact_handler
}  # type: dict[str, Callable[..., Any]]


def load_config(path=DEBUG_INI_PATH):
    # type: (str) -> RawConfigParser
    config = RawConfigParser()
    config.read(path)
    return config


def load_handler_config(name, config):
    # type: (str, RawConfigParser) -> dict[str, str] | None
    if config.has_section(name) and config.getboolean(name, "Enabled"):
        return {
            k.lower(): v
            for k, v in config.items(name)
            if k.lower() != "enabled"
        }
    return None


def debug_signal_handler(sig, frame):
    # type: (int, FrameType) -> None
    """Default debug signal handler.

    Might raise EINTR/IOError when occuring during some syscalls on Python 2.
    """
    print("\n# Entering debug signal handler...\n\nTraceback:\n{}\n".format(
        "".join(traceback.format_stack(frame))
    ))
    try:
        config = load_config()
    except Exception:
        traceback.print_exc()
        print("\n# Aborting debug signal handler...\n")
        return

    for handler_name, handler_callback in DEBUG_HANDLERS.items():
        try:
            handler_config = load_handler_config(handler_name, config)
            if handler_config is not None:
                print("\nTrying handler `{}`".format(handler_name))
                print(" - handler config = `{}`\n".format(handler_config))
                handler_callback(sig, frame, **handler_config)
                break
        except Exception:
            traceback.print_exc()
    else:
        print("\nNo handler found!\n")
    print("\n# Exiting debug signal handler...\n")


def register_debug_signal(fn=debug_signal_handler):
    # type: (Callable[..., Any]) -> None
    """Register a debug handler on SIGBREAK (Windows) or SIGUSR1 (Linux).

    On Windows, press CTRL+Pause/Break to trigger.
    On Linux, send a SIGUSR1 signal.

    Will raise ValueError exception if not called from the main thread.
    """
    if hasattr(signal, "SIGBREAK"):
        signal.signal(signal.SIGBREAK, fn)  # type: ignore
    else:
        signal.signal(signal.SIGUSR1, fn)  # type: ignore


def dry_run(delay=10.):
    # type: (float) -> None
    """Dry run test."""
    from threading import Timer

    if TYPE_CHECKING or PYTHON_VERSION == 3:
        from _thread import interrupt_main
    else:
        from thread import interrupt_main

    Timer(delay, interrupt_main).start()
