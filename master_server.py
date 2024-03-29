#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Monster Hunter master server.

    Monster Hunter 3 Server Project
    Copyright (C) 2021  Sepalani

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import threading

import opn_server as OPN
import lmp_server as LMP
import fmp_server as FMP
import rfp_server as RFP

from other.utils import create_server_from_base


def create_servers(silent=False):
    """Create servers and check if it has ui."""
    servers = []
    has_ui = False
    for module in (OPN, LMP, FMP, RFP):
        server, has_window = create_server_from_base(*module.BASE,
                                                     silent=silent)
        has_ui = has_ui or has_window
        servers.append(server)
    return servers, has_ui


def main(args):
    """Master server main function."""
    servers, has_ui = create_servers(silent=args.silent)
    threads = [
        threading.Thread(target=server.serve_forever)
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
        for server in servers:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interactive", action="store_true",
                        dest="interactive",
                        help="create an interactive shell")
    parser.add_argument("-s", "--silent", action="store_true",
                        dest="silent",
                        help="silent console logs")
    args = parser.parse_args()
    main(args)
