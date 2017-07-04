import pygame
import sys
from pygame.locals import *
from random import random, choice, randint
import math


pygame.init()



BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

OPTIONS = [BLACK, WHITE, RED, GREEN, BLUE]
COLORS = []
INDEX = 0

infoObject = pygame.display.Info()
FPS = 30
WIDTH = infoObject.current_w
HEIGHT = infoObject.current_h
fpsClock = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
ballx = int(WIDTH / 2)
bally = int(HEIGHT / 2)
ball_pos =(ballx, bally)
RADIUS = int(round(((WIDTH/2)**2 + (HEIGHT/2)**2)**0.5, 0))
R = 0
G = 0
B = 0
H = 0
new_color = [(R, G, B)]
CIRCLES = []
STEPS = 0
step = 3
DIRECTION = 1
cJump = 10

while STEPS <= RADIUS:
    COLORS.append(BLACK)
    CIRCLES.append(STEPS)
    STEPS += step


def randcolor():
    return (randint(0,255), randint(0,255), randint(0,255))

def intColor(arvo):
    r = arvo & 255
    g = (arvo >> 8) & 255
    b = (arvo >> 16) & 255
    return (r, g, b)

def sinebow(h):
	h += 1/float(2)
	h *= -1
	r = math.sin(math.radians(math.pi * h))

	g = math.sin(math.radians(math.pi * (h + 20)))
	b = math.sin(math.radians(math.pi * (h + 45)))
	return (int(255.0*r**2.0), int(255.0*g**2.0), int(255.0*b**2.0))

allC = 0
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    """if DIRECTION == 1:
        if R < 255:
            R += cJump
        elif G < 255:
            G += cJump
        elif B < 255:
            B += cJump
        else:
            DIRECTION = 0
    else:
            if R > 0:
                R -= cJump
            elif G > 0:
                G -= cJump
            elif B > 0:
                B -= cJump
            else:
                DIRECTION = 1
    if R > 255:
        R = 255
    elif R < 0:
        R = 0
    elif G > 255:
        G = 255
    elif G < 0:
        G = 0
    elif B > 255:
        B = 255
    elif B < 0:
        B = 0
        """
    new_color = sinebow(H)
    H = (H+1)%360
    COLORS = COLORS[1:] + [new_color]
    INDEX = 0

    for i in reversed(CIRCLES):
        pygame.draw.circle(DISPLAYSURF, COLORS[INDEX], ball_pos, i)
        INDEX = (INDEX + 1)%RADIUS
    pygame.display.update()

    fpsClock.tick(FPS)
