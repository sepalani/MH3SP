#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2021-2025 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Monster Hunter master server."""

import sys
import threading
import traceback

import opn_server as OPN
import lmp_server as LMP
import fmp_server as FMP
import rfp_server as RFP

from other.debug import register_debug_signal, dry_run
from other.python import TYPE_CHECKING
from other.utils import create_server_from_base

if TYPE_CHECKING:
    from argparse import Namespace  # noqa: F401
    from collections.abc import Sequence  # noqa: F401
    from typing import Any  # noqa: F401

    from mh.server import BasicPatServer  # noqa: F401


def create_servers(server_args):
    # type: (Sequence[str]) -> tuple[list[BasicPatServer], bool]
    """Create servers and check if it has ui."""
    servers = []  # type: list[BasicPatServer]
    has_ui = False
    for module in (OPN, LMP, FMP, RFP):
        server, args = create_server_from_base(*module.BASE,
                                               cmd_args=server_args)  # type: ignore[misc]  # noqa: E501
        if server and args:
            has_ui = has_ui or args.log_to_window
            servers.append(server)
    return servers, has_ui


def main(args):
    # type: (Namespace) -> None
    """Master server main function."""
    register_debug_signal()

    servers, has_ui = create_servers(server_args=args.args)
    threads = [
        threading.Thread(
            target=server.serve_forever,
            name="{}.serve_forever".format(server.__class__.__name__)
        )
        for server in servers
    ]
    # TODO: Backport cache's logic (i.e. new thread, maintain_connection)

    def interactive_mode(local=locals()):
        # type: (dict[str, Any]) -> None
        """Run an interactive python interpreter in another thread."""
        import code
        code.interact(local=local)

    repl_thread = threading.Thread(target=interactive_mode)

    if has_ui:
        from other.ui import update as ui_update
    else:
        def ui_update():
            pass

    try:
        ui_update()
        for server_thread in threads:
            server_thread.start()

        if args.interactive:
            repl_thread.start()

        if args.dry_run:
            dry_run()

        while threads:
            for server_thread in threads:
                ui_update()
                if not server_thread.is_alive():
                    threads.remove(server_thread)
                    break
                server_thread.join(0.1)

    except KeyboardInterrupt:
        print("Interrupt key was pressed, closing servers...")
    except Exception:
        print('Unexpected exception caught...')
        traceback.print_exc()
        sys.exit(1)
    finally:
        for server in servers:
            server.close()
        if args.interactive and repl_thread.is_alive():
            repl_thread.join()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interactive", action="store_true",
                        dest="interactive",
                        help="create an interactive shell")
    parser.add_argument("--dry-run", action="store_true",
                        dest="dry_run",
                        help="dry run to test the server")
    # TODO: Backport central/cache parameters (server_id, no_timeout)
    #  - no_timeout is currently available as a server argument as follows:
    parser.add_argument("args", nargs='*',
                        help="arguments forwarded to all servers")
    args = parser.parse_args()
    main(args)
