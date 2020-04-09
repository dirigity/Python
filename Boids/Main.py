import pygame
from pygame.locals import *
import numpy as np
import math

NEGRO = (0, 0 ,0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VIOLETA = (98, 0, 255)

#[pos,V]
_Data = [[[400,400],[0,-1]],[[200,200],[0,-1]]]
_DesingSkin = ((0,1),(.5,0),(-.5,0))
size = 20
_skin = [(a[0]*size,a[1]*size) for a in _DesingSkin]
_timeHold = 0

def main():
    global _Data
    quit = False
    size = (700, 500)
    screen = pygame.display.set_mode(size,HWSURFACE|DOUBLEBUF|RESIZABLE)
    pygame.display.set_caption("UnPureRef")
    while not quit :
        screen.fill(NEGRO)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
            elif event.type==pygame.VIDEORESIZE:
                screen=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
                pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                leftclick, middleclick, rightclick = pygame.mouse.get_pressed()
                timeHold = timeHold+1
                if(rightclick):
                    if timeHold == 0 or timeHold > 10:
                        Pos = pygame.mouse.get_pos()
                        _Data.append([Pos,[0,0]])
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                timeHold = 0
        #move

        _Data = [[[b[0][0]+b[1][0],b[0][1]+b[1][1]],b[1]] for b in _Data]

        #draw
        for Boid in _Data:
            skin = getSkin(Boid)
            print(skin)
            pygame.draw.polygon(screen, VERDE, skin)

        pygame.display.update()


def getSkin(Boid):
    a = angle(Boid[1],[0,1])
    TurnedSkin = [rotate((0,0),p,a) for p in _skin]
    return [[Boid[0][0]+pos[0],Boid[0][1]+pos[1]] for pos in TurnedSkin]


def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))


def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

main()
pygame.quit()