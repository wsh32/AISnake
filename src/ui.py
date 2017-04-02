#!/usr/bin/env python

"""ui.py: User Interface for the snake"""

import sys

import pygame

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
GRAY = (80, 80, 80)
DARK_GRAY = (40, 40, 40)
ORANGE = (255, 155, 111)

BGCOLOR = BLACK
GRID_COLOR = DARK_GRAY
SNAKE_COLOR = WHITE
APPLE_COLOR = RED
TEXT_COLOR = GREEN
BG_TEXT_COLOR = GRAY

SNAKE2_COLOR = BLUE

START = pygame.K_b

UP = pygame.K_UP
DOWN = pygame.K_DOWN
LEFT = pygame.K_LEFT
RIGHT = pygame.K_RIGHT
QUIT = pygame.K_q

UP2 = pygame.K_w
DOWN2 = pygame.K_s
LEFT2 = pygame.K_a
RIGHT2 = pygame.K_d

RESET = pygame.K_r


class GridUI:
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

    def draw_grid(self):
        for x in range(self.outside_margin, self.window_width, self.segment_size+self.segment_margin):
            pygame.draw.line(self.screen, GRID_COLOR, (x, self.outside_margin),
                             (x, self.window_height - self.outside_margin), self.segment_margin)
        for y in range(self.outside_margin, self.window_height+self.outside_margin, self.segment_size+self.segment_margin):
            pygame.draw.line(self.screen, GRID_COLOR, (self.outside_margin, y),
                             (self.window_width - self.outside_margin, y), self.segment_margin)

    def fill_cell(self, x, y, color):
        if 0 <= x < self.cells_width and 0 <= y < self.cells_height:
            rect_x = x * self.total_segment + self.outside_margin + self.segment_margin
            rect_y = y * self.total_segment + self.outside_margin + self.segment_margin
            rectangle = pygame.Rect(rect_x, rect_y, self.segment_size, self.segment_size)
            pygame.draw.rect(self.screen, color, rectangle)

    def draw_apple(self, apple, color):
        self.fill_cell(apple.get_x(), apple.get_y(), color)

    def draw_snake(self, snake, color):
        for i in snake.get_coords():
            self.fill_cell(i.get_x(), i.get_y(), color)

    def draw_text(self, text, border):
        text = self.font.render(text, True, TEXT_COLOR)
        text_rect = text.get_rect(center=(self.window_width/2, self.window_height/2))

        bg_rect_x = self.window_width/2 - text.get_rect().width/2 - border
        bg_rect_y = self.window_height/2 - text.get_rect().height/2 - border
        bg_rect_w = text.get_rect().width + 2*border
        bg_rect_h = text.get_rect().height + 2*border
        rectangle = pygame.Rect(bg_rect_x, bg_rect_y, bg_rect_w, bg_rect_h)

        pygame.draw.rect(self.screen, BG_TEXT_COLOR, rectangle)

        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def title(self, title):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.draw_text(title, 10)


class SinglePlayerUI(GridUI):
    def __init__(self, cells_width, cells_height, segment_size, segment_margin, outside_margin, fps):
        super().__init__(cells_width, cells_height, segment_size, segment_margin, outside_margin, fps)

        self.game = SinglePlayerGame(cells_width, cells_height)
        self.winner = 2

    def go(self):
        self.title("Single Player Snake! Press 'b' to begin!")
        while self.winner == 2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == START:
                        self.winner = 0
        self.play()

    def play(self):
        self.game = SinglePlayerGame(self.cells_width, self.cells_height)
        while self.winner == 0:
            self.update()
        while self.winner == 1:
            self.draw_text("You lose! Score: " + str(self.game.get_snake().get_length()), 10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == RESET:
                        self.winner = 0
                        break
                    elif event.key == QUIT:
                        sys.exit(0)
        self.play()

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

        self.draw_apple(self.game.get_apple(), APPLE_COLOR)
        self.draw_snake(self.game.get_snake(), SNAKE_COLOR)

        if not self.game.update(direction):
            self.winner = 1
        else:
            pygame.display.flip()

        self.fps_clock.tick(self.fps)


class TwoPlayerUI(GridUI):
    def __init__(self, cells_width, cells_height, segment_size, segment_margin, outside_margin, fps):
        super().__init__(cells_width, cells_height, segment_size, segment_margin, outside_margin, fps)

        self.game = TwoPlayerGame(cells_width, cells_height)
        self.winner = 3

    def go(self):
        while self.winner == 3:
            self.title("Two Player Snake! Press 'b' to begin!")
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == START:
                        self.winner = 0
        self.play()

    def play(self):
        while self.winner == 0:
            self.update()
        while self.winner == 1 or self.winner == 2:
            self.draw_text("Player " + str(self.winner) + " wins! Press 'r' to play again or press 'q' to quit!", 10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == RESET:
                        self.winner = 0
                        break
                    elif event.key == QUIT:
                        sys.exit(0)
        self.play()

    def update(self):
        # This function should be run every repetition
        # Reset screen
        self.screen.fill(BGCOLOR)
        self.draw_grid()

        direction_1 = False
        direction_2 = False

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == QUIT:
                    sys.exit(0)
                elif event.key == UP:
                    direction_1 = Direction.UP
                elif event.key == DOWN:
                    direction_1 = Direction.DOWN
                elif event.key == LEFT:
                    direction_1 = Direction.LEFT
                elif event.key == RIGHT:
                    direction_1 = Direction.RIGHT
                elif event.key == UP2:
                    direction_2 = Direction.UP
                elif event.key == DOWN2:
                    direction_2 = Direction.DOWN
                elif event.key == LEFT2:
                    direction_2 = Direction.LEFT
                elif event.key == RIGHT2:
                    direction_2 = Direction.RIGHT

        if not self.game.update(direction_1, direction_2):
            if self.game.alive_s1 and not self.game.alive_s2:
                self.winner = 1
            elif self.game.alive_s2 and not self.game.alive_s1:
                self.winner = 2
        else:
            self.winner = 0
            self.draw_apple(self.game.get_apple(), APPLE_COLOR)
            self.draw_snake(self.game.get_snake_1(), SNAKE_COLOR)
            self.draw_snake(self.game.get_snake_2(), SNAKE2_COLOR)

            pygame.display.flip()

        self.fps_clock.tick(self.fps)
