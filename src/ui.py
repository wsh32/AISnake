#!/usr/bin/env python

"""ui.py: User Interface for the snake"""

import pygame, sys
from snake import *

__author__ = "Wesley Soo-Hoo"
__license__ = "MIT"

# Globals
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
PINK = (198, 134, 156)
BLACK = (17, 18, 13)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 155, 0)
DARK_GRAY = (40, 40, 40)
ORANGE = (255, 155, 111)

BGCOLOR = BLACK
GRID_COLOR = DARK_GRAY
SNAKE_COLOR = WHITE
APPLE_COLOR = RED

UP = pygame.K_UP
DOWN = pygame.K_DOWN
LEFT = pygame.K_LEFT
RIGHT = pygame.K_RIGHT
QUIT = pygame.K_q


class SinglePlayerUI:
    def __init__(self, cells_width, cells_height, segment_size, segment_margin, outside_margin, fps):
        self.segment_size = segment_size
        self.segment_margin = segment_margin
        self.total_segment = segment_margin + segment_size
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

        self.game = SinglePlayerGame(cells_width, cells_height)

    def update(self):
        # This function should be run every repetition
        # Reset screen
        self.screen.fill(BGCOLOR)
        self.draw_grid()

        direction = False

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == QUIT:
                    sys.exit(0)
                elif event.key == UP:
                    direction = Direction.UP
                elif event.key == DOWN:
                    direction = Direction.DOWN
                elif event.key == LEFT:
                    direction = Direction.LEFT
                elif event.key == RIGHT:
                    direction = Direction.RIGHT

        if not self.game.update(direction):
            print("YOU DIED")
        else:
            self.draw_apple(self.game.get_apple())
            self.draw_snake(self.game.get_snake())

            pygame.display.flip()

        self.fps_clock.tick(self.fps)

    def draw_grid(self):
        for x in range(self.outside_margin, self.window_width, self.segment_size+self.segment_margin):
            pygame.draw.line(self.screen, GRID_COLOR, (x, self.outside_margin),
                             (x, self.window_height - self.outside_margin), self.segment_margin)
        for y in range(self.outside_margin, self.window_height+self.outside_margin, self.segment_size+self.segment_margin):
            pygame.draw.line(self.screen, GRID_COLOR, (self.outside_margin, y),
                             (self.window_width - self.outside_margin, y), self.segment_margin)

    def fill_cell(self, x, y, color):
        if 0 <= x < self.cells_width and 0 <= y < self.cells_height:
            rect_x = x * self.total_segment + self.outside_margin + self.segment_margin - 1
            rect_y = y * self.total_segment + self.outside_margin + self.segment_margin - 1
            rectangle = pygame.Rect(rect_x, rect_y, self.segment_size, self.segment_size)
            pygame.draw.rect(self.screen, color, rectangle)

    def draw_apple(self, apple):
        self.fill_cell(apple.get_x(), apple.get_y(), APPLE_COLOR)

    def draw_snake(self, snake):
        for i in snake.get_coords():
            self.fill_cell(i.get_x(), i.get_y(), SNAKE_COLOR)

