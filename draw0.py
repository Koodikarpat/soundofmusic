import pygame
from pygame import surfarray
import sys
from pygame.locals import *
from random import random, choice, randint
from math import sin, radians, degrees, asin
import numpy as np




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
SCREEN = np.zeros((WIDTH, HEIGHT, 3))
DISPLAYSURF = pygame.display.set_mode(SCREEN.shape[:2], 0, 32)

#center of the screen
ballx = int(WIDTH / 2)
bally = int(HEIGHT / 2)
ball_pos =(ballx, bally)

#calculates radious from center to corner
RADIUS = int(round(((WIDTH/2)**2 + (HEIGHT/2)**2)**0.5, 0))

#degrees for making colors. poor name I admit. Increment tells how much degrees rize every cycle. VAIHE sets the difference of
#different sine waves
H = 0
INCREMENT = 5
VAIHE = 30

#list of circles. Amount of circles counted by step size.

STEPS = 0
step = 6

#creates the cirles and initializes their color as black
"""for y in range(HEIGHT):
    line = []
    for x in range(WIDTH):
        line.append(BLUE)
    SCREEN.append(line)"""

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
    g = sin(radians(h + VAIHE))*int(225/2.0) + 225/2.0
    b = sin(radians(h + VAIHE*2))*int(225/2.0) + 225/2.0
    return (r,g,b)

def distance(arr, point):
    grid_x, grid_y = np.mgrid[0:arr.shape[0], 0:arr.shape[1]]
    circle = (grid_x - point[0]) ** 2 + (grid_y - point[1]) ** 2
    return circle**0.5

sinif = lambda x: sin(x)
sinif = np.vectorize(sinif)
degrify = lambda x: (degrees(asin(x))**2)**0.5
degrify = np.vectorize(degrify)

dist = distance(SCREEN, (100, 200))
dist2 = distance(SCREEN, (1000,200))
max1 = np.amax(dist)
max2 = np.amax(dist2)

adder1 = lambda x: (x-10)%max1
adder1 = np.vectorize(adder1)
adder2 = lambda x: (x-10)%max2
adder2 = np.vectorize(adder2)

sins1 = sinif(dist)
sins2 = sinif(dist2)
sins = (sins1+sins2)/2.0*-1
real = degrify(sins)


colorizer = np.vectorize(sinebow)
ar,ab,ag = colorizer(real)
rad = 0
toler = 10
SCREEN[:] = (0,0,0)
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    selections = np.logical_and(dist < rad + toler, dist > rad - toler)
    color = sinebow(H)
    SCREEN[:,:,0] = ar
    SCREEN[:,:,1] = ab
    SCREEN[:,:,2] = ag


    H = (H+INCREMENT)%360

    #removes last color and adds a new one to the top
    """COLORS = COLORS[1:] + [new_color]
    INDEX = 0"""

    #draws the circles

    surfarray.blit_array(DISPLAYSURF, SCREEN)
    pygame.display.flip()
    pygame.display.set_caption("name")
    rad += 5
    """for i in reversed(CIRCLES):
        pygame.draw.circle(DISPLAYSURF, COLORS[INDEX], ball_pos, i)
        INDEX = (INDEX + 1)%RADIUS"""
    dist = adder1(dist)
    dist2 = adder2(dist2)
    sins1 = sinif(dist)
    sins2 = sinif(dist2)
    sins = (sins1+sins2)/2.0
    real = degrify(sins)
    ar,ab,ag = colorizer(real)

    fpsClock.tick(FPS)
