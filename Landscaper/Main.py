from PIL import Image
import copy 
import random
import math as m
import numpy as np
import random
#from Landscaper 
import PerlingNoiseMagic as PN

random.seed(0)

size = 500 # Size of the map (in pixels)
scale = 3 # afects the size of the noise(biguer scale, smaler wrincles), only in tileable mode
tileable = True #Makes the map tileable, but it slows the proces majorly (also the slope detection doesnt work on not tilible borders, so you will need to remove a litle bit from the border of the image manualy or proceduraly on your 3d sofware of choice)
DisolveConstant = 1/10 # Should be betwen 0 and 1 highter makes deeper trenches as drops walk
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
    retValue = map[x%size][y%size]
    retOriginalValue = OriginalLevel[x%size][y%size]
    for pos in rets:
        posValue = map[ret[0]][ret[1]]
        posOriginalValue = OriginalLevel[ret[0]][ret[1]]
        if 10*max(0,posOriginalValue-posValue)+posValue < 10*max(0,retOriginalValue-retValue)+retValue:
            ret = pos
            retValue = posValue
            retOriginalValue = posOriginalValue

    return ret

def main():

    print("Generating Ground Noise")
    pnFact = PN.PerlinNoiseFactory(4,octaves = 4) #greater octaves makes more detailed noise at cost of speed
    if tileable :
        Height = [[pnFact(m.cos((j/size)*2*m.pi)/scale,m.sin((j/size)*2*m.pi)/scale,m.cos((i/size)*2*m.pi)/scale,m.sin((i/size)*2*m.pi)/scale) for i in range(size)] for j in range(size)]
    else:
        Height = [[pnFact(0,0,i,j) for i in range(size)] for j in range(size)]
    Height = normaliceArr(Height,100)
    OriginalLevel = copy.deepcopy(Height) # Used for takin into acount the top soil level in terrain solubility

    itterations = 10000 # number of rain droplets to simulate
    print("Starting Erosion")

    I = 0
    while(I<itterations):
        #create droplet at random place
        DropX = random.randint(0,size)%size
        DropY = random.randint(0,size)%size
        waterContent = 500 # one Water content can disolve one Soil content && one water content will be removed from the droplet one each 1/EvaporationRate steps
        SoilContent = 0
        while (waterContent>0):
            #print (SoilContent,waterContent)
            #put in the ground if saturated
            if SoilContent > waterContent:
                if((SoilContent-waterContent)>1):
                    print("sedimenting:"+str((SoilContent-waterContent)))
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
                #print("residue:"+str(residue))
                #print(Height[DropX][DropY])
                Height[DropX][DropY] = Height[DropX][DropY] - residue
                #print(Height[DropX][DropY] - residue)
                SoilContent = SoilContent + residue
            #evaporate
            waterContent = waterContent - (EvaporationRate*max(((DropX-NextX)**2+(DropY-NextY)**2)**.5,1))

            #step
            DropX = NextX
            DropY = NextY
            
        if(I%(100)==0):
            print(I/itterations)
            d = 10
            if(I%(itterations/d)==0):
                print("---TakingSnapShot---")
                imageFromHeight(Height,(I/itterations)*d)

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
    #Normalice and convert to image (as we only hace 256 posible hight states we normalice to get the maximum detail out of them)

    NormData = normaliceArr(Height,2**16).astype(np.uint32)
    # Convert to image
    im = Image.fromarray(NormData)
    im.save("render"+str(tag)+".png")
main()
