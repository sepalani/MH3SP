#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2021-2024 MH3SP Server Project
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
from other.utils import create_server_from_base


def create_servers(silent=False, debug_mode=False):
    """Create servers and check if it has ui."""
    servers = []
    has_ui = False
    for module in (OPN, LMP, FMP, RFP):
        server, has_window = create_server_from_base(*module.BASE,
                                                     silent=silent,
                                                     debug_mode=debug_mode)
        has_ui = has_ui or has_window
        servers.append(server)
    return servers, has_ui


def main(args):
    """Master server main function."""
    register_debug_signal()

    servers, has_ui = create_servers(silent=args.silent,
                                     debug_mode=args.debug_mode)
    threads = [
        threading.Thread(
            target=server.serve_forever,
            name="{}.serve_forever".format(server.__class__.__name__)
        )
        for server in servers
    ]
    for thread in threads:
        thread.start()

    def interactive_mode(local=locals()):
        """Run an interactive python interpreter in another thread."""
        import code
        code.interact(local=local)

    if has_ui:
        from other.ui import update as ui_update
        ui_update()

    try:
        if args.interactive:
            t = threading.Thread(target=interactive_mode)
            t.start()

        if args.dry_run:
            dry_run()

        while threads:
            for thread in threads:
                if has_ui:
                    ui_update()
                if not thread.is_alive():
                    threads.remove(thread)
                    break
                thread.join(0.1)

        if args.interactive:
            t.join()
    except KeyboardInterrupt:
        print("Interrupt key was pressed, closing server...")
    except Exception:
        print('Unexpected exception caught...')
        traceback.print_exc()
        sys.exit(1)
    finally:
        for server in servers:
            server.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interactive", action="store_true",
                        dest="interactive",
                        help="create an interactive shell")
    parser.add_argument("-s", "--silent", action="store_true",
                        dest="silent",
                        help="silent console logs")
    parser.add_argument("-d", "--debug_mode", action="store_true",
                        dest="debug_mode",
                        help="enable debug mode, disabling timeouts and \
                        lower logging verbosity level")
    parser.add_argument("--dry-run", action="store_true",
                        dest="dry_run",
                        help="dry run to test the server")
    args = parser.parse_args()
    main(args)
