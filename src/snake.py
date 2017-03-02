#!/usr/bin/env python

"""snake.py: Non GUI game logic"""

from enum import Enum
import random

__author__ = "Wesley Soo-Hoo"
__license__ = "MIT"


class SinglePlayerGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.last_direction = Direction.LEFT

        self.snake = Snake(int(width/2), int(height/2))
        apple_coords = self.generate_apple_coords()
        self.apple = Segment(apple_coords[0], apple_coords[1])
        self.apple_triggered = False
        self.alive = True

    def generate_apple_coords(self):
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if not self.snake.collided((x, y)):
                print("Generating new apple", x, y)
                return x, y
        return False

    def get_apple(self):
        return self.apple

    def get_snake(self):
        return self.snake

    def is_alive(self):
        return self.alive

    def update(self, direction):
        if not direction:
            current_direction = self.last_direction
        elif (self.last_direction == Direction.UP and direction == Direction.DOWN) or \
            (self.last_direction == Direction.DOWN and direction == Direction.UP) or \
            (self.last_direction == Direction.LEFT and direction == Direction.RIGHT) or \
            (self.last_direction == Direction.RIGHT and direction == Direction.LEFT):
            current_direction = self.last_direction
        else:
            self.last_direction = current_direction = direction

        self.snake.update(current_direction, self.apple_triggered)

        self.apple_triggered = self.apple.collided(self.snake.get_head().get_position())
        if self.apple_triggered:
            apple_coords = self.generate_apple_coords()
            self.apple.set_position(apple_coords[0], apple_coords[1])

        if self.snake.suicide():
            self.alive = False
        elif self.snake.get_head().get_x() < 0:
            self.alive = False
        elif self.snake.get_head().get_x() >= self.width:
            self.alive = False
        elif self.snake.get_head().get_y() < 0:
            self.alive = False
        elif self.snake.get_head().get_y() >= self.height:
            self.alive = False

        return self.alive


class TwoPlayerGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Snake:
    def __init__(self, startx, starty):
        self.direction = Direction.LEFT
        self.coords = [
            Segment(startx, starty),
            Segment(startx + 1, starty),
            Segment(startx + 2, starty),
        ]

    def get_coords(self):
        return self.coords

    def get_head(self):
        return self.coords[0]

    def suicide(self):
        head = self.get_head().get_position()
        for i in range(1, len(self.coords)):
            if self.coords[i].collided(head):
                return True
        return False

    def collided(self, pos):
        for i in self.coords:
            if i.collided(pos):
                return True
        return False

    def get_length(self):
        return len(self.coords)

    def update(self, direction, apple):
        if direction:
            self.direction = direction

        last_coords_a = self.coords[0].get_position()
        last_coords_b = self.coords[0].get_position()
        self.coords[0].update(direction)

        for i in range(1, len(self.coords)):
            if i % 2 == 0:
                last_coords_b = self.coords[i].get_position()
                self.coords[i].set_position(last_coords_a[0], last_coords_a[1])
            else:
                last_coords_a = self.coords[i].get_position()
                self.coords[i].set_position(last_coords_b[0], last_coords_b[1])
            last_coords = self.coords[i].get_position()

        if apple:
            self.coords.append(Segment(last_coords[0], last_coords[1]))


class Segment:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = True

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_position(self):
        return self.x, self.y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def update(self, direction):
        if direction == Direction.UP:
            self.up()
        elif direction == Direction.DOWN:
            self.down()
        elif direction == Direction.LEFT:
            self.left()
        elif direction == Direction.RIGHT:
            self.right()

    def left(self):
        self.x -= 1

    def right(self):
        self.x += 1

    def up(self):
        self.y -= 1

    def down(self):
        self.y += 1

    def is_active(self):
        return self.active

    def enable(self, active):
        self.active = active

    def disable(self, active):
        self.active = active

    def collided(self, position):
        return self.x == position[0] and self.y == position[1]
