#!/usr/bin/env python

"""main.py: This is where the magic happens"""

import ui

__author__ = "Wesley Soo-Hoo"
__license__ = "MIT"


if __name__ == '__main__':
    spui = ui.SinglePlayerUI(15, 10, 30, 1, 5, 60)
    spui.draw_grid()
    while True:
        pass
