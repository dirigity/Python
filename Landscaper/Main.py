from PIL import Image
import copy 
import random
import math as m
import numpy as np
import time
import datetime

#from Landscaper 
#import PerlingNoiseMagic as PN
from opensimplex import OpenSimplex
import sys
from multiprocessing import Pool


random.seed(0)
quality = 0.1 # Qualities lower than 1 mean a really limited droplet sim, I would recomend a 3 or 4 level
size = 400 # Size of the map (in pixels)
scale = 5 # afects the size of the noise(smaller scale, smaler wrincles), only in tileable mode
tileable = True #Makes the map tileable (the slope detection doesnt work on not tilible borders, so you will need to remove a litle bit from the border of the image manualy or proceduraly on your 3d sofware of choice to avoid artefacts)
DisolveConstant = 1/2 # Should be betwen 0 and 1 (highter makes deeper trenches as drops walk)
EvaporationRate = 0.2 # bigger than 0


def findSlope(x,y,map,OriginalLevel):
    rets = [
    [(x-1)  %size,(y-1) %size],
    [x      %size,(y-1) %size],
    [(x+1)  %size,(y-1) %size],
    [(x-1)  %size,y     %size],
    [(x+1)  %size,y     %size],
    [(x-1)  %size,(y+1) %size],
    [x      %size,(y+1) %size],
    [(x+1)  %size,(y+1) %size]
    ]
    ret = [x%size,y%size]
    #print(x,y)
    retValue = map[x%size][y%size]
    retOriginalValue = OriginalLevel[x%size][y%size]
    n = 10
    for pos in rets:
        posValue = map[pos[0]][pos[1]]
        posOriginalValue = OriginalLevel[pos[0]][pos[1]]
        if n*max(0,posOriginalValue-posValue)+posValue < n*max(0,retOriginalValue-retValue)+retValue:
            ret = pos
            retValue = posValue
            retOriginalValue = posOriginalValue

    return ret

def NoiseRow(IN):
    j = IN[0]
    pnFact = IN[1]
    if(j%10==0):
        print("Progres:"+str(j/size)) #as it is multitheaded the logs are kid of all over the place, but gives you a kind of sense of progress
    x = m.cos((j/size)*2*m.pi)/scale
    y = m.sin((j/size)*2*m.pi)/scale
    return [noise(pnFact,x,y,m.cos((i/size)*2*m.pi)/scale,m.sin((i/size)*2*m.pi)/scale) for i in range(size)]

def noise(s,x,y,z,w):
    ret = 0
    octaves = 4
    for i in range(1,octaves):
        ret = ret + s.noise4d(x*(i**2),y*(i**2),z*(i**2),w*(i**2))/(i**2)
    return ret

def InitialPos(i,tot,size):
    if(i < (i- i%(size**2))/size**2 ):
        #print("sqr")
        row = (i-(i%size))/size
        return(int(row),int(i-(size*(row))))
    else:
        #print("rnd")
        return(random.randint(0,size)%size,random.randint(0,size)%size)


def main():
    Height = []
    print("Generating Ground Noise")
    #pnFact = PN.PerlinNoiseFactory(4,octaves = 4) #greater octaves makes more detailed noise at cost of speed
    tmp = OpenSimplex()
    if tileable :
        #Height = [[pnFact(m.cos((j/size)*2*m.pi)/scale,m.sin((j/size)*2*m.pi)/scale,m.cos((i/size)*2*m.pi)/scale,m.sin((i/size)*2*m.pi)/scale) for i in range(size)] for j in range(size)]

        p = Pool(4)
        Height = p.map(NoiseRow, [(j,tmp) for j in range(size)])

    else:
        Height = [[tmp.noise2d(i,j) for i in range(size)] for j in range(size)]
    Height = normaliceArr(Height,100)
    OriginalLevel = copy.deepcopy(Height) # Used for taking into acount the top soil level in terrain solubility

    itterations = (size**2)*quality # number of rain droplets to simulate
    print("Starting Erosion")

    I = 0
    print("Droplets to Simulate:"+str(itterations))
    
    StartMillis = time.time() * 1000

    while(I<itterations):
        
        #create droplet at random place
        
        IPos = InitialPos(I,itterations,size)
        DropX = IPos[0]#random.randint(0,size)%size
        DropY = IPos[1]#random.randint(0,size)%size
        waterContent = 300 # one Water content can disolve one Soil content && one water content will be removed from the droplet one each 1/EvaporationRate steps
        SoilContent = 0

        while (waterContent>0):
            #print (SoilContent,waterContent)
            #put in the ground if saturated
            if SoilContent > waterContent:
                #print("Precipito")
                Height[DropX][DropY] = Height[DropX][DropY]+(SoilContent-waterContent)
                SoilContent = waterContent

            nextPos = findSlope(DropX,DropY,Height,OriginalLevel)
            NextX=nextPos[0]
            NextY=nextPos[1]
            #print(DropX,DropY,NextX,NextY)

            #take from the ground if not saturated

            if SoilContent < waterContent:
                solubility = min(1,1/(1+OriginalLevel[DropX][DropY]-Height[DropX][DropY])) #based on how much has been removed from this position because soil is easier to remove than rock
                maximum = Height[DropX][DropY] - Height[NextX][NextY]
                        
                residue = DisolveConstant*maximum*solubility
                #print("residue:"+str(DropX)+"-"+str(DropY)+"-"+str(NextX)+"-"+str(NextY))
                #print(Height[DropX][DropY])
                Height[DropX][DropY] = Height[DropX][DropY] - residue
                #print(Height[DropX][DropY])
                #SoilContent = SoilContent + residue
            #evaporate
            waterContent = waterContent - (EvaporationRate*max(((DropX-NextX)**2+(DropY-NextY)**2)**.5,1))

            #step
            DropX = NextX
            DropY = NextY

        

        Leap = 100
        if(I%Leap==0):
            EndMillis = time.time() * 1000

            print("Simulation Progress: ["+str(100*(I/itterations))+"%]")
            print("Estimated time left: ["+str(datetime.timedelta(seconds=((EndMillis-StartMillis)/Leap)*(itterations-I)))+"]")
            StartMillis = time.time() * 1000

            d = 10
            if(I%(itterations/d)==0):
                print("---Taking SnapShot ["+str((I/itterations)*(d))+"]---")
                imageFromHeight(Height,(I/itterations)*d)
                print("---Resuming Simulation---")


        I = I + 1
    DiferenceMap = [[Height[x][y]-OriginalLevel[x][y] for y in range(size)]for x in range(size)]

    print("Procesing Output")

    imageFromHeight(Height,"Final")
    imageFromHeight(DiferenceMap,"Difference")

def normaliceArr (arr,NewMax):
    v = []
    for row  in arr:
        for e in row:
            v.append(e)
    Min = min(v)
    Max = max(v)
    if(Min==Max):
        return np.array(arr)
    return np.array([ [ NewMax*((o-Min)/(Max-Min)) for o in row ] for row in arr])


def imageFromHeight(Height,tag):

    NormData = normaliceArr(Height,2**16).astype(np.uint32)
    # Convert to image
    im = Image.fromarray(NormData)
    im.save("render"+str(tag)+".png")

main()
sys.stdout = open("Out.txt", "w")




