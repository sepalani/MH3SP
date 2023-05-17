#! /usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright (C) 2021 MH3SP Server Project
# SPDX-License-Identifier: AGPL-3.0-or-later
"""UI helper module."""

import logging
try:
    # Python 3.x
    import tkinter as tk
    import tkinter.scrolledtext as ScrolledText
    from queue import Queue
except ImportError:
    # Python 2.x
    import Tkinter as tk
    import ScrolledText
    from Queue import Queue

WINDOWS = []
EMITTERS = Queue()


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

        # Won't work on Python3.x
        # self.text.after(0, append)
        EMITTERS.put(lambda: self.text.after(0, append))


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
    while not EMITTERS.empty():
        f = EMITTERS.get()
        f()
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
