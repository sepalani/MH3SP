#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2021-2022 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Monster Hunter master server."""

import threading
import traceback

import opn_server as OPN
import lmp_server as LMP
import fmp_server as FMP
import rfp_server as RFP

from other.debug import register_debug_signal
from other.utils import create_server_from_base

from other.cache import Cache

def create_servers(server_id, silent=False, debug_mode=False, no_timeout=False):
    """Create servers and check if it has ui."""
    servers = []
    has_ui = False
    for module in ((OPN, LMP, FMP, RFP) if server_id==0 else (FMP,)):
        server, has_window = create_server_from_base(*module.BASE,
                                                     server_id=server_id,
                                                     silent=silent,
                                                     debug_mode=debug_mode,
                                                     no_timeout=no_timeout)
        has_ui = has_ui or has_window
        servers.append(server)
    return servers, has_ui


def main(args):
    """Master server main function."""
    servers, has_ui = create_servers(server_id=args.server_id,
                                     silent=args.silent,
                                     debug_mode=args.debug_mode,
                                     no_timeout=args.no_timeout)
    threads = [
        threading.Thread(
            target=server.serve_forever,
            name="{}.serve_forever".format(server.__class__.__name__)
        )
        for server in servers
    ]
    cache = Cache(server_id=args.server_id, debug_mode=args.debug_mode,
                log_to_file=True, log_to_console=not args.silent,
                log_to_window=False)
    threads.append(threading.Thread(target=cache.maintain_connection))
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
                        help="enable debug mode, \
                        raising logging verbosity level")
    parser.add_argument("-t", "--no_timeout", action="store_true",
                        dest="no_timeout",
                        help="disable player timeouts")
    parser.add_argument("-S", "--server_id", type=int, default=0,
                        dest="server_id",
                        help="specifies the server id used to pull info \
                        from the config file (0 for central)")

    args = parser.parse_args()
    main(args)
