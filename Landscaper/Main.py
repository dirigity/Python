from PIL import Image
import copy 
import random
import math as m
import numpy as np
import random


size, freq, octs = 500, 1/200, 3 #smaler freq means biguer mountains 


DisolveConstant = 1/10 # Should be betwen 0 and 1 highter makes deeper trenches as drops walk
EvaporationRate = 0.2 # bigger than 0

def noiseArrNoTileable():


    shape = (500,500) # texture size (Height,Width)
    scale = 400.0
    octaves = 4
    persistence = 0.5
    lacunarity = 2.0

    n = 0
    world = [[0 for y in range(size)]for x in range(size)]
    for i in range(size):
        for j in range(size):
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

perm = list(range(size*2))
random.shuffle(perm)
perm += perm
dirs = [(m.cos(a * 2.0 * m.pi / size*2),
        m.sin(a * 2.0 * m.pi / size*2))
        for a in range(size*2)]

def noise(x, y, per):
    def surflet(gridX, gridY):
        distX, distY = abs(x-gridX), abs(y-gridY)
        polyX = 1 - 6*distX**5 + 15*distX**4 - 10*distX**3
        polyY = 1 - 6*distY**5 + 15*distY**4 - 10*distY**3
        hashed = perm[perm[int(gridX)%per] + int(gridY)%per]
        grad = (x-gridX)*dirs[hashed][0] + (y-gridY)*dirs[hashed][1]
        return polyX * polyY * grad
    intX, intY = int(x), int(y)
    return (surflet(intX+0, intY+0) + surflet(intX+1, intY+0) +
            surflet(intX+0, intY+1) + surflet(intX+1, intY+1))

def fBm(x, y, per, octs):
    val = 0
    for o in range(octs):
        val += 0.5**o * noise(x*2**o, y*2**o, per*2**o)
    return val







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
    for pos in rets:
        if 10*OriginalLevel[pos[0]][pos[1]]+map[pos[0]][pos[1]] < 10*OriginalLevel[ret[0]][ret[1]]+map[ret[0]][ret[1]]:
            ret = pos

    return ret

def main():

    print("Generating Ground Noise")
    Height = [[fBm(x*freq, y*freq, int(size*freq), octs) for x in range(size)] for y in range(size)]


    Height = normaliceArr(Height,100)
    OriginalLevel = copy.deepcopy(Height) # Used for takin into acount the top soil level in terrain solubility

    itterations = 1000 # number of rain droplets to simulate
    print("Starting Erosion")

    I = 0
    while(I<itterations):
        #create droplet at random place
        DropX = random.randint(0,size)%size
        DropY = random.randint(0,size)%size
        waterContent = 300 # one Water content can disolve one Soil content && one water content will be removed from the droplet one each 1/EvaporationRate steps
        SoilContent = 0
        while (waterContent>0):
            #print (SoilContent,waterContent)
            #put in the ground if saturated
            if SoilContent > waterContent:
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
                print("-----")
                imageFromHeight(Height,(I/itterations)*d)

        I = I + 1
    DiferenceMap = [[Height[x][y]-OriginalLevel[x][y] for y in range(size)]for x in range(size)]

    imageFromHeight(Height,"Final")
    imageFromHeight(DiferenceMap,"Difference")

def normaliceArr (arr,NewMax):
    v = []
    for row  in arr:
        for e in row:
            v.append(e)
    Min = min(v)
    Max = max(v)
    return np.array([ [ NewMax*((e-Min)/(Max-Min)) for e in row ] for row in arr])

def imageFromHeight(Height,tag):
    #Normalice and convert to image (as we only hace 256 posible hight states we normalice to get the maximum detail out of them)

    NormData = normaliceArr(Height,2**16).astype(np.uint32)
    # Convert to image
    im = Image.fromarray(NormData)
    im.save("render"+str(tag)+".png")
main()
