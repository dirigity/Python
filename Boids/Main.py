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
_Data = [
            
        ]
_DesingSkin = ((0,1),(.5,0),(-.5,0))
size = 20
_skin = [(a[0]*size,a[1]*size) for a in _DesingSkin]
_StarPos = []
_EndPos = []
_Folowing = False
_MousePos = []
_TimePresed = 0
_timeThreshold = 100
MaxV = 7
def main():
    global _timeThreshold
    global _TimePresed
    global _Data
    global _StarPos
    global _EndPos
    global _MousePos
    global _Folowing
    quit = False
    Atraction = False
    _size = (700, 500)
    screen = pygame.display.set_mode(_size,HWSURFACE|DOUBLEBUF|RESIZABLE)
    pygame.display.set_caption("Boids")
    while not quit :
        _MousePos = pygame.mouse.get_pos()
        screen.fill(NEGRO)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
            elif event.type==pygame.VIDEORESIZE:
                _size = event.dict['size']
                screen=pygame.display.set_mode(_size,HWSURFACE|DOUBLEBUF|RESIZABLE)
                pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                leftclick, middleclick, rightclick = pygame.mouse.get_pressed()
                if(leftclick):
                    _StarPos = _MousePos
                    _TimePresed = 1
                elif(rightclick):
                    Atraction = True
                
            elif event.type == pygame.MOUSEBUTTONUP:
                Atraction = False
                if(_TimePresed<_timeThreshold):
                    _EndPos = _MousePos
                    V = [(_EndPos[i]-_StarPos[i])/100 for i in range(len(_EndPos))]
                    _Data.append([_StarPos,V])
                _TimePresed = -1

        if (_TimePresed > 0):
            _TimePresed += 1
            if _TimePresed > _timeThreshold and _TimePresed%40 == 0:
                _EndPos = _MousePos
                V = [(_EndPos[i]-_StarPos[i])/100 for i in range(len(_EndPos))]
                _Data.append([_StarPos,V])
                    

        #move

        _Data = [ [ [ (b[0][0] + b[1][0])%_size[0] , (b[0][1] + b[1][1])%_size[1] ] ,b[1] ] for b in _Data]

        for i,Boid in enumerate(_Data):
            force = ForceTo(i,Boid)
            if(Atraction):
                force = AtractionAlg(force,_MousePos,i)
            _Data[i][1] = [_Data[i][1][0] + force[0], _Data[i][1][1] + force[1]]

            _Data[i][1] = [a*min(MaxV,length(_Data[i][1])) for a in normalice(_Data[i][1])]
            


        #draw
        for Boid in _Data:
            skin = getSkin(Boid)
            pygame.draw.polygon(screen, VERDE, skin)

        pygame.display.update()


def normalice(V):
    l = length(V)
    if(l != 0):
        return [a/l for a in V]
    return V

def AtractionAlg(F,Pos,i):
    ret = F
    ret[0] = ret[0] + forceFromDistance(Pos[0]-_Data[i][0][0]) 
    ret[1] = ret[1] + forceFromDistance(Pos[1]-_Data[i][0][1]) 
    return ret


def getSkin(Boid):
    a = angle(Boid[1],[0,1])
    TurnedSkin = [rotate((0,0),p,a) for p in _skin]
    return [[Boid[0][0]+pos[0],Boid[0][1]+pos[1]] for pos in TurnedSkin]

def ForceTo(i,Boid):
    global _Data
    ret = [0,0]
    for I,B in enumerate(_Data):
        if(I!=i):
            ret[0] = ret[0] + forceFromDistance(B[0][0]-Boid[0][0])
            ret[1] = ret[1] + forceFromDistance(B[0][1]-Boid[0][1])
    return ret


def forceFromDistance(x):
    ret = math.log10(abs(x))
    if(x>0):
        return ret
    return -ret
    



def dotproduct(v1, v2):
    return sum((a*b) for a, b in zip(v1, v2))

def length(v):
    return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
    d = (length(v1) * length(v2))
    if(d!=0):
        return math.acos(dotproduct(v1, v2) / d)
    else:
        return 0

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