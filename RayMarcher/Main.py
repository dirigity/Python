from copy import deepcopy
import math as m1
import numpy as np
import time
from PIL import Image
from multiprocessing import Pool


#import sys
#sys.stdout = open("Out.txt", "w")




# ObjetName,Bounds,posX,posY,posZ,R,G,B,Rough,additional
# Sfere,r,posX,PosY,Posz,R,G,B,rough
# Cube,Bounds,posX,PosY,Posz,R,G,B,rough


# Point,PosX,PosY,PosZ,rad,R,G,B,Bri
# Sun,AngleX,AngleY,R,G,B,I
SKY = [70,70,70]
CERO = 0.000001
INF = 1000000000
maxSteps = 1000
maxDistance = 1000
objects=[["Cube",(100,0.1,100),0,-0.5,0,100,255,255,1],["Cube",(1,1,1),0,0,1,255,255,100,1],["Sfere",1,0,0.7,-1,100,255,100,1],["Sfere",1,0,0,-1,255,100,255,1]]#
lights=[["Point",-2,3,-0.3,0.3,255,255,255,1.4],["Point",1,2,1,0.3,255,255,255,0.2],["Sun",(1,1,1),255,255,255,0.3]]


def VectorFromAngle(aX,aY):
    # assert aY >= -m1.pi/2 and aY <= m1.pi/2
    # assert aX >= -m1.pi and aX <= m1.pi
    x=m1.cos(aX)*m1.sin(aY)
    y=m1.cos(aX)*m1.cos(aY)
    z=m1.sin(aX)
    return normalize(x,y,z)

def Ray(cx,cy,cz,dir,bounces):
    x = cx
    y = cy
    z = cz
    OBJ = []
    #Chocar con objeto
    hit = False
    StepCounter = 0
    maxDistance = 100 #MAXdistance(z,y,x)

    while not hit and maxSteps > StepCounter and maxDistance > PointDistance(x,y,z,cx,cy,cz):
        dInfo = MINdistance(x,y,z)
        d = dInfo[0]
        x = x + dir[0]*d
        y = y + dir[1]*d
        z = z + dir[2]*d
        if(d<CERO):
            hit = True
            OBJ = objects[dInfo[1]]
            x = x - dir[0]*d
            y = y - dir[1]*d
            z = z - dir[2]*d
        StepCounter = StepCounter + 1 

    if not hit:
        return SKY           

    SurfaceR = OBJ[5]/255
    SurfaceG = OBJ[6]/255
    SurfaceB = OBJ[7]/255

    colorR = SKY[0]*SurfaceR
    colorG = SKY[1]*SurfaceG
    colorB = SKY[2]*SurfaceB
    if bounces is 0:
        #ir a luces
        for lam in lights:
            V = [0,0,1]
            if(lam[0]=="Sun"):# Sun,V,R,G,B,I


                V = lam[1]
                intensityR = lam[2]
                intensityG = lam[3]
                intensityB = lam[4]
                brightness = lam[5]
            
                hit = False
                ilum = False
                lx = x + V[0] * 0.01
                ly = y + V[1] * 0.01
                lz = z + V[2] * 0.01

                while not hit and not ilum:
                    d = MINdistance(lx,ly,lz)[0]

                    lx = lx + V[0]*d
                    ly = ly + V[1]*d
                    lz = lz + V[2]*d

                    if d<CERO :
                        hit = True
                    elif PointDistance(lx,ly,lz,cx,cy,cz)>maxDistance :
                        ilum = True
                        colorR = colorR + SurfaceR*abs(intensityR*brightness * m1.cos(angle(V,Normal(x,y,z,OBJ)))) 
                        
                        colorG = colorG + SurfaceG*abs(intensityG*brightness * m1.cos(angle(V,Normal(x,y,z,OBJ)))) 

                        colorB = colorB + SurfaceB*abs(intensityB*brightness * m1.cos(angle(V,Normal(x,y,z,OBJ)))) 

            if(lam[0]=="Point"):
                vx = -(x-lam[1])
                vy = -(y-lam[2])
                vz = -(z-lam[3])
                l = PointDistance(0,0,0,vx,vy,vz)
                V = [vx/l,vy/l,vz/l]
                intensityR = lam[5]
                intensityG = lam[6]
                intensityB = lam[7]
                brightness = lam[8]
            
                hit = False
                ilum = False
                lx = x + vx * 0.01
                ly = y + vy * 0.01
                lz = z + vz * 0.01

                while not hit and not ilum:


                    d = MINdistanceObjLamp(lx,ly,lz,lam)

                    lx = lx + V[0]*d
                    ly = ly + V[1]*d
                    lz = lz + V[2]*d

                    if d<CERO :
                        hit = True
                    elif PointDistance(lx,ly,lz,lam[1],lam[2],lam[3])<lam[4] :
                        ilum = True
                        colorR = colorR + SurfaceR*abs(intensityR*brightness * m1.cos(angle(V,Normal(x,y,z,OBJ))) * 1/PointDistance(x,y,z,lam[1],lam[2],lam[3])) 
                        
                        colorG = colorG + SurfaceG*abs(intensityG*brightness * m1.cos(angle(V,Normal(x,y,z,OBJ))) * 1/PointDistance(x,y,z,lam[1],lam[2],lam[3])) 

                        colorB = colorB + SurfaceB*abs(intensityB*brightness * m1.cos(angle(V,Normal(x,y,z,OBJ))) * 1/PointDistance(x,y,z,lam[1],lam[2],lam[3])) 
                    
                    
        #implement ambient Oclusion
        r = min(colorR*((1/(StepCounter+1)/1000)+1),250)
        g = min(colorG*((1/(StepCounter+1)/1000)+1),250)
        b = min(colorB*((1/(StepCounter+1)/1000)+1),250)
        return (r,g,b)
    else:
        bounces = bounces - 1
        bounceVecotors = bounceVectors(dir,normalizeTuple(Normal(x,y,z,OBJ)),OBJ[8])
        r = SKY[0]*SurfaceR
        g = SKY[1]*SurfaceG
        b = SKY[2]*SurfaceB
        for VBounce in bounceVecotors:
            c = Ray(x,y,z,VBounce,bounces)
            r = min(r + c[0] ,250) #* ((SurfaceR-1)/1)+1)
            g = min(g + c[1] ,250) #* ((SurfaceG-1)/1)+1)
            b = min(b + c[2] ,250) #* ((SurfaceB-1)/1)+1)
        return (r,g,b)

def bounceVectors(Vdir,Vnor,R):
    l = len(Vdir)
    #Vdir -( 2 * (Vdir * Vnor )*Vnor)
    Res2 = tuple(dotproduct(Vdir,Vnor)*Vnor[j] for j in range(l))
    Res1 = tuple(2*Res2[j] for j in range(l))
    center = tuple(Vdir[i] - Res1[i] for i in range(l))
    return [center]

def dotproduct(v1, v2):
    return sum((a*b) for a, b in zip(v1, v2))

def length(v):
    return (dotproduct(v, v))**.5

def angle(v1, v2):
    if(length(v1) * length(v2)==0):
        print(v1,v2)
    a = dotproduct(v1, v2) / (length(v1) * length(v2))
    if(a<-1):
        a = -1
    elif(a>1):
        a = 1
    return m1.acos(a)

def PointDistance(x1,y1,z1,x2,y2,z2):
    A = x1-x2
    B = y1-y2
    C = z1-z2
    return (A*A + B*B + C*C)**.5

def Normal(x,y,z,OBJ):
    # Sfere,Rad,posX,PosY,Posz
    if(OBJ[0]=="Sfere"):
        rX = (x-OBJ[2])
        rY = (y-OBJ[3])
        rZ = (z-OBJ[4])
        return (rX,rY,rZ)
    elif(OBJ[0]=="Cube"):
        s = OBJ[1]
        rX = (x-OBJ[2])/(s[0]/2)
        rY = (y-OBJ[3])/(s[1]/2)
        rZ = (z-OBJ[4])/(s[2]/2)

        vx = 0
        vy = 0
        vz = 0

        margin = 0.0001

        if(rX>=1-margin):
            vx = 1
        elif(rX<=-1+margin):
            vx = -1
        
        if(rY>=1-margin):
            vy = 1
        elif(rY<=-1+margin):
            vy = -1
        
        if(rZ>=1-margin):
            vz = 1
        elif(rZ<=-1+margin):
            vz = -1
        
        if(vx == 0 and vy == 0 and vz == 0):
            print(OBJ,x,y,z,rX,rY,rZ)
        
        return (vx,vy,vz)

    


def MINdistanceObjLamp(x,y,z,l):
    return min(PointDistance(x,y,z,l[1],l[2],l[3]),MINdistance(x,y,z)[0])

def MINdistance(x,y,z):
    rets = distanceList(x,y,z)
    ret = INF
    I = 0
    Index = 0
    for r in rets:
        if(r<ret): 
            I = Index
            ret = r
        Index = Index+1
    
    return [ret,I]

def MAXdistance(x,y,z):
    rets = distanceList(x,y,z)
    ret = 0

    for rindex in range(len(rets)):
        r = rets[rindex]+length(objects[rindex][1])*2
        if(r>ret): 
            ret = r
    
    return ret

def distanceTo(obj,x,y,z):
    if(obj[0]=="Sfere"):
        return PointDistance(x,y,z,obj[2],obj[3],obj[4])-(obj[1]/2)
    if(obj[0]=="Cube"):
        #max{0,|x|−1}^2+max{0,|y|−1}^2+max{0,|z|−1}^2
        s = obj[1]
        rX = (x-obj[2])
        rY = (y-obj[3])
        rZ = (z-obj[4])
        pX = max(0,abs(rX)-(s[0]/2))
        pY = max(0,abs(rY)-(s[1]/2))
        pZ = max(0,abs(rZ)-(s[2]/2))
        return PointDistance(0,0,0,pX,pY,pZ)

    return INF


def distanceList(x,y,z):
    return [distanceTo(obj,x,y,z) for obj in objects]

def render(x,y,z,multiProz,w,h):
    StartMillis = int(round(time.time() * 1000))


    PreData = [ (b,x,y,z,w,h) for b in range(h) ]


    #columnN = 0
    #for column in data:
    #    elementN = 0
    #    
    #    for element in column:
    #        Vx = -1
    #        Vy = (columnN/len(data)*sensorL)-sensorL/2
    #        Vz = (elementN/len(column)*sensorL)-sensorL/2
    #        d = PointDistance(Vx,Vy,Vz,0,0,0)
    #        data[columnN][elementN]=Ray(x,y,z,Vx/d,Vy/d,Vz/d,0)
    #        elementN = elementN+1
    #    columnN = columnN+1

    if multiProz:
        p = Pool(4)
        data = p.map(threadRay, PreData)
    else:
        data = [ threadRay(Line) for Line in PreData]



    
    EndMillis = int(round(time.time() * 1000))
    print(EndMillis-StartMillis)
    img = Image.fromarray(np.asarray(data,dtype=np.uint8), 'RGB' )

    return img
# 0 1 2 3 4 5
#(b,x,y,z,w,h)
def threadRay(d):
    print(d)
    w=d[4]
    h=d[5]
    antires = 1/1000
    sensorW = antires * w
    sensorH = antires * h

    columnN = d[0]
    x,y,z = d[1],d[2],d[3]

    #ret = []
    
    #elementN = 0
    #for element in range(w):
    #    Vx = -1
    #    Vy = ((columnN/h)*sensorH)-(sensorH/2)
    #    Vz = ((elementN/w)*sensorW)-(sensorW/2)
    #    ret.append(Ray(x,y,z,normalize(Vx,Vy,Vz),0))
    #    elementN = elementN+1

    aX = 0
    aY = 0
    aZ = 0.5

    return [ Ray(x,y,z,rotateVAngleXYZ(normalize(-1,((columnN/-h)*sensorH)+(sensorH/2),((elementN/w)*sensorW)-(sensorW/2)),aX,aY,aZ),0) for elementN in range(w)]

def normalize(x,y,z):
    l = PointDistance(0,0,0,x,y,z)
    return (x/l,y/l,z/l)

def normalizeTuple(V):
    x = V[0]
    y = V[1]
    z = V[2]
    l = PointDistance(0,0,0,x,y,z)
    return (x/l,y/l,z/l)

def rotateVAngleXYZ(v,aX,aY,aZ):
    return np.dot(rotation_matrix((0,0,1), aZ), np.dot(rotation_matrix((0,1,0), aY), np.dot(rotation_matrix((1,0,0), aX), v)))

def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / m1.sqrt(np.dot(axis, axis))
    a = m1.cos(theta / 2.0)
    b, c, d = -axis * m1.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

def main():
    aspectRatio = (16,9)
    m = 100
    img = render(5,3,0,True,aspectRatio[0]*m,aspectRatio[1]*m)
    img.save('render.png')

    img.show()




main()
