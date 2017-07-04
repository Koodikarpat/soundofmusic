import pygame
import sys
from pygame.locals import *
from random import random, choice, randint
from math import sin, radians


pygame.init()


#basic colors used in testing
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

OPTIONS = [BLACK, WHITE, RED, GREEN, BLUE]
COLORS = []
INDEX = 0

infoObject = pygame.display.Info()
FPS = 60
#fullscreen
WIDTH = infoObject.current_w
HEIGHT = infoObject.current_h
fpsClock = pygame.time.Clock()
#window
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

#center of the screen
ballx = int(WIDTH / 2)
bally = int(HEIGHT / 2)
ball_pos =(ballx, bally)

#calculates radious from center to corner
RADIUS = int(round(((WIDTH/2)**2 + (HEIGHT/2)**2)**0.5, 0))

#degrees for making colors. poor name I admit. Increment tells how much degrees rize every cycle
H = 0
INCREMENT = 4

#list of circles. Amount of circles counted by step size.
CIRCLES = []
STEPS = 0
step = 3

#creates the cirles and initializes their color as black
while STEPS <= RADIUS:
    COLORS.append(BLACK)
    CIRCLES.append(STEPS)
    STEPS += step

#returns random colors.
def randcolor():
    return (randint(0,255), randint(0,255), randint(0,255))

#takes regular number and returns its hex color as rgb
def intColor(arvo):
    r = arvo & 255
    g = (arvo >> 8) & 255
    b = (arvo >> 16) & 255
    return (r, g, b)

#colors on a sine wave
def sinebow(h):

    r = sin(radians(h))*int(225/2.0) + 225/2.0
    g = sin(radians(h + 120))*int(225/2.0) + 225/2.0
    b = sin(radians(h + 240))*int(225/2.0) + 225/2.0
    return (r,g,b)

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    new_color = sinebow(H)
    H = (H+INCREMENT)%360

    #removes last color and adds a new one to the top
    COLORS = COLORS[1:] + [new_color]
    INDEX = 0

    #draws the circles
    for i in reversed(CIRCLES):
        pygame.draw.circle(DISPLAYSURF, COLORS[INDEX], ball_pos, i)
        INDEX = (INDEX + 1)%RADIUS
    pygame.display.update()

    fpsClock.tick(FPS)
