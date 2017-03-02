#!/usr/bin/env python

"""main.py: This is where the magic happens"""

import ui

__author__ = "Wesley Soo-Hoo"
__license__ = "MIT"


if __name__ == '__main__':
    spui = ui.SinglePlayerUI(20, 15, 30, 1, 5, 10)
    while True:
        spui.update()
