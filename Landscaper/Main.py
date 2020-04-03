import imageio as io
from PIL import Image

import math as m
import noise
import numpy as np
import random

shape = (500,500) # texture size (Height,Width)
scale = 400.0
octaves = 4
persistence = 0.5
lacunarity = 2.0
DisolveConstant = 9 # Should be betwen 0 and 1
EvaporationRate = 1 # bigger than 0

def noiseArr():
    n = 0
    world = [[0 for y in range(shape[1])]for x in range(shape[0])]
    for i in range(shape[0]):
        for j in range(shape[1]):
            n = noise.pnoise2(i/scale, 
                              j/scale, 
                              octaves=octaves, 
                              persistence=persistence, 
                              lacunarity=lacunarity, 
                              repeatx=1024, 
                              repeaty=1024, 
                              base=0)
            world[i][j] = n
            
    return world

def findSlope(x,y,map):
    rets = [
    [(x-1)  %shape[0],(y-1) %shape[1]],
    [x      %shape[0],(y-1) %shape[1]],
    [(x+1)  %shape[0],(y-1) %shape[1]],
    [(x-1)  %shape[0],y     %shape[1]],
    [(x+1)  %shape[0],y     %shape[1]],
    [(x-1)  %shape[0],(y+1) %shape[1]],
    [x      %shape[0],(y+1) %shape[1]],
    [(x+1)  %shape[0],(y+1) %shape[1]]
    ]
    ret = [x%shape[0],y%shape[1]]
    for pos in rets:
        if (map[pos[0]][pos[1]]) < (map[ret[0]][ret[1]]):
            ret = pos

    return ret

def main():

    Height = normaliceArr(noiseArr())
    OriginalLevel = Height # Used for takin into acount the top soil level in terrain solubility

    itterations = 1000 # number of rain droplets to simulate

    I = 0
    while(I<itterations):
        #create droplet at random place
        DropX = random.randint(0,shape[0])%shape[0]
        DropY = random.randint(0,shape[1])%shape[1]
        waterContent = 1 # one Water content can disolve one Soil content && one water content will be removed from the droplet one each 1/EvaporationRate steps
        SoilContent = 0
        while (waterContent>0):

            #put in the ground if saturated
            if SoilContent > waterContent:
                Height[DropX][DropY] = Height[DropX][DropY]+(SoilContent-waterContent)
                SoilContent = waterContent

            nextPos = findSlope(DropX,DropY,Height)
            NextX=nextPos[0]
            NextY=nextPos[1]

            #take from the ground if not saturated

            if SoilContent < waterContent:
                solubility = min(1,1/(1+OriginalLevel[DropX][DropY]-Height[DropX][DropY])) #based on how much has been removed from this position because soil is easier to remove than rock
                maximum = Height[DropX][DropY] - Height[NextX][NextY]
                        
                residue = DisolveConstant*maximum*solubility

                #print(DropX,DropY,NextX,NextY,residue)
                #print(Height[DropX][DropY])
                Height[DropX][DropY] = Height[DropX][DropY] - residue
                #print(Height[DropX][DropY] - residue)
                SoilContent = SoilContent + residue
            #evaporate
            waterContent = waterContent - (EvaporationRate*max(((DropX-NextX)**2+(DropY-NextY)**2)**.5,0.1))

            #step
            DropX = NextX
            DropY = NextY
            
        if(I%(itterations/10)==0):
            print(I/itterations)
            d = 10
            if(I%(itterations/d)==0):
                print("-----")
                imageFromHeight(Height,(I/itterations)*d)

        I = I + 1
    DiferenceMap = [[Height[x][y]-OriginalLevel[x][y] for y in range(shape[1])]for x in range(shape[0])]

    imageFromHeight(Height,"Final")
    imageFromHeight(DiferenceMap,"Difference")

def normaliceArr (arr):
    v = []
    for row  in arr:
        for e in row:
            v.append(e)
    Min = min(v)
    Max = max(v)+0.01
    print(Min,Max)
    return np.array([ [ (2**16)*((e-Min)/(Max-Min)) for e in row ] for row in arr]).astype(np.uint32)

def imageFromHeight(Height,tag):
    #Normalice and convert to image (as we only hace 256 posible hight states we normalice to get the maximum detail out of them)

    NormData = normaliceArr(Height)
    # Convert to image
    im = Image.fromarray(NormData)
    im.save("render"+str(tag)+".png")
main()
