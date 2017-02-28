#!/usr/bin/env python

"""test.py: Testing the pygame library to make sure it is usable.
The documentation for this is here: https://www.pygame.org/docs/"""

import sys, pygame

pygame.init()

size = width, height = 640, 480
speed = [2, 1]

UP = pygame.K_UP
DOWN = pygame.K_DOWN
LEFT = pygame.K_LEFT
RIGHT = pygame.K_RIGHT

QUIT = pygame.K_q

black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

FPS = 120
FPS_CLOCK = pygame.time.Clock()

screen = pygame.display.set_mode(size)


def test():
    ball = pygame.image.load("ball.gif")
    ballrect = ball.get_rect()

    pygame.init()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit(0)

        ballrect = ballrect.move(speed)
        if ballrect.left < 0 or ballrect.right > width:
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]

        screen.fill(black)
        screen.blit(ball, ballrect)
        pygame.display.flip()
        FPS_CLOCK.tick(FPS)


def key():
    pygame.init()

    font = pygame.font.SysFont("monospace", 15)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == LEFT:
                    screen.fill(black)
                    label = font.render("Left", 1, (255, 255, 0))
                    screen.blit(label, (width/2, height/2))
                elif event.key == RIGHT:
                    screen.fill(black)
                    label = font.render("Right", 1, (255, 255, 0))
                    screen.blit(label, (width/2, height/2))
                elif event.key == QUIT:
                    sys.exit(0)
        pygame.display.flip()
        FPS_CLOCK.tick(FPS)


if __name__ == '__main__':
    key()
