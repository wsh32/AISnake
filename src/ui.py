#!/usr/bin/env python

"""ui.py: User Interface for the snake"""

import pygame

__author__ = "Wesley Soo-Hoo"
__license__ = "MIT"

# Globals
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
PINK = (198, 134, 156)
BLACK = (17, 18, 13)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 155, 0)
DARK_GRAY = (40, 40, 40)
ORANGE = (255, 155, 111)
BGCOLOR = BLACK

UP = pygame.K_UP
DOWN = pygame.K_DOWN
LEFT = pygame.K_LEFT
RIGHT = pygame.K_RIGHT


class SinglePlayerUI:
    def __init__(self, cells_width, cells_height, segment_size, segment_margin, outside_margin, fps):
        self.segment_size = segment_size
        self.segment_margin = segment_margin
        self.outside_margin = outside_margin

        self.cells_width = cells_width
        self.cells_height = cells_height

        self.window_height = self.cells_height * (self.segment_size + self.segment_margin) \
                             + self.segment_margin + self.outside_margin * 2
        self.window_width = self.cells_width * (self.segment_size + self.segment_margin) \
                            + self.segment_margin + self.outside_margin * 2

        pygame.init()

        self.font = pygame.font.SysFont("roboto", 30)
        self.fps = fps
        self.fps_clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

    def draw_grid(self):
        self.screen.fill(BGCOLOR)
        for x in range(self.outside_margin, self.window_width, self.segment_size+self.segment_margin):
            pygame.draw.line(self.screen, DARK_GRAY, (x, self.outside_margin),
                             (x, self.window_height - self.outside_margin), self.segment_margin)
        for y in range(self.outside_margin, self.window_height+self.outside_margin, self.segment_size+self.segment_margin):
            pygame.draw.line(self.screen, DARK_GRAY, (self.outside_margin, y),
                             (self.window_width - self.outside_margin, y), self.segment_margin)
        pygame.display.flip()
        self.fps_clock.tick(self.fps)
