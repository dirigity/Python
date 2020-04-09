import pygame
from pygame.locals import *

import os

pygame.init()


NEGRO = (0, 0 ,0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VIOLETA = (98, 0, 255)

Imgs = [[[10,10],"render0.0.png"],[[100,10],"render1.0.png"],[[10,100],"render2.0.png"],]
SelectedImg = ""
_image_library = {}
def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                image = pygame.image.load(path)
                _image_library[path] = image
        return image

def main():
    global Imgs
    size = (700, 500)
    screen = pygame.display.set_mode(size,HWSURFACE|DOUBLEBUF|RESIZABLE)
    pygame.display.set_caption("UnPureRef")


    hecho = False

    reloj = pygame.time.Clock()

    sliding = False
    StartPos = 0,0
    EndPos = 0,0


    while not hecho:
        pygame.event.pump()

        screen.fill(NEGRO)
        for e in pygame.event.get(): 
            if e.type == pygame.QUIT: 
                hecho = True 
            elif e.type==pygame.VIDEORESIZE:
                screen=pygame.display.set_mode(e.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
                pygame.display.flip()
            #elif e.type == pygame.KEYDOWN:
            #elif e.type == pygame.KEYUP:
            elif e.type == pygame.MOUSEBUTTONDOWN:
                leftclick, middleclick, rightclick = pygame.mouse.get_pressed()

                if(leftclick):
                    sliding = True
                    SelectedImg = "All"
                    StartPos = pygame.mouse.get_pos()
                elif(rightclick):
                    sliding = True
                    StartPos = pygame.mouse.get_pos()
                    SelectedImg = "All"
                    print(Imgs)
                    for i,Test in enumerate(Imgs):
                        size = get_image(Test[1]).get_size()
                        if(StartPos[0]>Test[0][0] and StartPos[0]<Test[0][0]+size[0]):
                            if(StartPos[1]>Test[0][1] and StartPos[1]<Test[0][1]+size[1]):
                                SelectedImg = i
                    if(SelectedImg!="All"):
                        wip = Imgs[SelectedImg]
                        Imgs.pop(SelectedImg)
                        Imgs.append(wip)
                   
            elif e.type == pygame.MOUSEBUTTONUP:
                sliding = False
                if(SelectedImg=="All"):
                    for img in Imgs:
                        EndPos = pygame.mouse.get_pos()
                        img[0][0] = img[0][0] + EndPos[0]-StartPos[0]
                        img[0][1] = img[0][1] + EndPos[1]-StartPos[1]
                else:
                    img = Imgs[len(Imgs)-1]
                    EndPos = pygame.mouse.get_pos()
                    img[0][0] = img[0][0] + EndPos[0]-StartPos[0]
                    img[0][1] = img[0][1] + EndPos[1]-StartPos[1]


        if(sliding):
            if(SelectedImg=="All"):
                for img in Imgs:
                    EndPos = pygame.mouse.get_pos()
                    newX = img[0][0] + EndPos[0]-StartPos[0]
                    newY = img[0][1] + EndPos[1]-StartPos[1]
                    screen.blit(get_image(img[1]), (newX,newY))
            else:
                for i,img in enumerate(Imgs):
                    if(i!=len(Imgs)-1):
                        EndPos = pygame.mouse.get_pos()
                        newX = img[0][0] 
                        newY = img[0][1] 
                        screen.blit(get_image(img[1]), (newX,newY))
                img = Imgs[len(Imgs)-1]
                EndPos = pygame.mouse.get_pos()
                newX = img[0][0] + EndPos[0]-StartPos[0]
                newY = img[0][1] + EndPos[1]-StartPos[1]
                screen.blit(get_image(img[1]), (newX,newY))
                
        else:
            for img in Imgs:
                screen.blit(get_image(img[1]), img[0])


        pygame.display.flip()

        reloj.tick(20)

    pygame.quit()


main()