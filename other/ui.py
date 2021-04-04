#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""UI helper module.

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

import logging
try:
    # Python 3.x
    import tkinter as tk
    import tkinter.scrolledtext as ScrolledText
except ImportError:
    # Python 2.x
    import Tkinter as tk
    import ScrolledText

WINDOWS = []


class LoggingHandler(logging.Handler):
    """This class allows to log to a Tkinter Text or ScrolledText widget.

    Adapted from:
     - https://stackoverflow.com/questions/13318742
     - https://gist.github.com/moshekaplan/c425f861de7bbf28ef06
    """

    def __init__(self, text):
        logging.Handler.__init__(self)
        self.text = text

    def emit(self, record):
        msg = self.format(record)

        def append():
            """Necessary because we can't modify it from other threads."""
            self.text.configure(state='normal')
            self.text.insert(tk.END, msg + '\n')
            self.text.configure(state='disabled')
            self.text.yview(tk.END)  # Autoscroll to the bottom

        self.text.after(0, append)


class LoggerTk(tk.Tk):
    """Create a logging window."""

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        text = ScrolledText.ScrolledText(self, state='disabled')
        text.configure(font='TkFixedFont')
        text.pack(expand=True, fill=tk.BOTH)

        global WINDOWS
        WINDOWS.append(self)

        self.handler = LoggingHandler(text)

    def get_handler(self):
        """Return the window's logging.Handler instance."""
        return self.handler

    def set_logger(self, logger):
        """Add the window's logging.Handler to the logger."""
        logger.addHandler(self.handler)

        def on_close():
            """Detach the handler if the window is closed."""
            global WINDOWS
            WINDOWS.remove(self)
            logger.removeHandler(self.handler)
            self.destroy()

        self.protocol("WM_DELETE_WINDOW", on_close)


def update():
    """Manually update logger windows."""
    for window in WINDOWS:
        window.update_idletasks()
        window.update()


if __name__ == "__main__":
    print("UI default logger test")
    fmt = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=fmt)

    t = LoggerTk()
    t.title("Tk Logger test")
    t.get_handler().setFormatter(logging.Formatter(fmt))
    t.set_logger(logging.getLogger())

    logging.info("Info log message")
