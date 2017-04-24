#!/usr/bin/env python

"""main.py: This is where the magic happens"""

import ui

__author__ = "Wesley Soo-Hoo"
__license__ = "MIT"


def single():
    spui = ui.SinglePlayerUI(15, 15, 30, 1, 5, 15)
    spui.go()


def double():
    tpui = ui.TwoPlayerUI(30, 20, 30, 1, 5, 10)
    tpui.go()


if __name__ == '__main__':
    double()
