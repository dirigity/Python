from pygame import gfxdraw
import math
from pygame.locals import *
from copy import deepcopy
import math as m1
from PIL import Image
import numpy as np
import pygame
import time


import sys


_EmptySceneData = []
_SceneContents = []
_SceneIlumination = []

Sky = [70,70,70]
CERO = 0.01
MaxDistance = 100

class OBJ:
    def __init__(self,_type,_Data):
        if _type == "Sfere":
            self.type = "Sfere"
            self.R,self.Col = _Data
        


class Point:
    def __init__(self,X_,Y_,Z_):
        self.X = X_
        self.Y = Y_
        self.Z = Z_
    def __add__(self,P):
        return Point(P.X+self.X,P.Y+self.Y,P.Z+self.Z)
    def __sub__(self,P):
        return Point(-P.X+self.X,-P.Y+self.Y,-P.Z+self.Z)
    def transform(self,V):
        return Point(self.X+V.Vx,self.Y+V.Vy,self.Z+V.Vz)
    def ToArray(self):
        return [self.X,self.Y,self.Z]
    def __str__(self):
        return "P:[X:"+str(self.X)+",Y:"+str(self.Y)+",Z:"+str(self.Z)+"]"
class Vector:
    def __init__(self,X_,Y_,Z_):
        self.Vx = X_
        self.Vy = Y_
        self.Vz = Z_
    def normalice(self,a):
        l = self.modulo()
        return Vector(self.Vx*a/l,self.Vy*a/l,self.Vz*a/l,)
    def toPoint(self):
        return Point(self.Vx,self.Vy,self.Vz)
    def ToArray(self):
        return [self.Vx,self.Vy,self.Vz]
    def fixVector(self,P):
        return Point(self.Vx+P.X,self.Vy+P.Y,self.Vz+P.Z)
    def __add__(self,V):
        return Point(V.Vx+self.Vx,V.Vy+self.Vy,V.Vz+self.Vz)
    def __str__(self):
        return "V:[X:"+str(self.Vx)+",Y:"+str(self.Vy)+",Z:"+str(self.Vz)+"]"
    def modulo(self):
        return math.sqrt(pow(self.Vx,2)+pow(self.Vy,2)+pow(self.Vz,2))
    def ScalarProduct(self, V):
        return self.Vx * V.Vx + self.Vy * V.Vy + self.Vz * V.Vz
    #def VectorialProduct(Self, V)
class Ray:
    def __init__(self,P1_,P2_):
        self.P0 = P1_
        self.V = Vector((P2_-P1_).X,(P2_-P1_).Y,(P2_-P1_).Z)
    def DistanceVectorToP(self,P):
        AuxP = PlaneFromNormalPoint(self.V,P)
        IntersectionPoint = AuxP.RIntersect(self)
        return VectorFromPP(IntersectionPoint,P)
    def GetPointFromLanda(self,a):
        return VectorFromArr([o + a*self.V.ToArray()[i] for i,o in enumerate(self.P0.ToArray())])
class Sphere:
    def __init__(self,P_,R_):
        self.P = P_
        self.r = R_
    def RayIntersection(self,ray,calculate):
        AuxV = ray.DistanceVectorToP(self.P)
        if(AuxV.modulo()<self.r):
            if(not calculate):
                return True
            else:
                r = self.r
                
                Vx,Vy,Vz = ray.V.ToArray()
                Px,Py,Pz = ray.P0.ToArray()
                Ox,Oy,Oz = self.P.ToArray()
                a1=-(sqrt((Vz**2+Vy**2+Vx**2)*r**2+(-Py**2+2*Oy*Py-Px**2+2*Ox*Px-Oy**2-Ox**2)*Vz**2+(((2*Py-2*Oy)*Pz-2*Oz*Py+2*Oy*Oz)*Vy+((2*Px-2*Ox)*Pz-2*Oz*Px+2*Ox*Oz)*Vx)*Vz+(-Pz**2+2*Oz*Pz-Px**2+2*Ox*Px-Oz**2-Ox**2)*Vy**2+((2*Px-2*Ox)*Py-2*Oy*Px+2*Ox*Oy)*Vx*Vy+(-Pz**2+2*Oz*Pz-Py**2+2*Oy*Py-Oz**2-Oy**2)*Vx**2)+(Pz-Oz)*Vz+(Py-Oy)*Vy+(Px-Ox)*Vx)/(Vz**2+Vy**2+Vx**2)
                a2=(sqrt((Vz**2+Vy**2+Vx**2)*r**2+(-Py**2+2*Oy*Py-Px**2+2*Ox*Px-Oy**2-Ox**2)*Vz**2+(((2*Py-2*Oy)*Pz-2*Oz*Py+2*Oy*Oz)*Vy+((2*Px-2*Ox)*Pz-2*Oz*Px+2*Ox*Oz)*Vx)*Vz+(-Pz**2+2*Oz*Pz-Px**2+2*Ox*Px-Oz**2-Ox**2)*Vy**2+((2*Px-2*Ox)*Py-2*Oy*Px+2*Ox*Oy)*Vx*Vy+(-Pz**2+2*Oz*Pz-Py**2+2*Oy*Py-Oz**2-Oy**2)*Vx**2)+(Oz-Pz)*Vz+(Oy-Py)*Vy+(Ox-Px)*Vx)/(Vz**2+Vy**2+Vx**2)
                return [VectorFromArr(a2),VectorFromArr(a1)]
        return False    
class Plane:
    def __init__(self,V1_,V2_,P0_):
        self.V1 = V1_
        self.V2 = V2_
        self.P0 = P0_
    def RIntersect(self, R):

        TerminosIndepes = Matrix([
            [R.P0.X-self.P0.X],
            [R.P0.Y-self.P0.Y],
            [R.P0.Z-self.P0.Z]
        ])
        Merme = Matrix([
            [-R.V.Vx,self.V1.Vx,self.V2.Vx],
            [-R.V.Vy,self.V1.Vy,self.V2.Vy],
            [-R.V.Vz,self.V1.Vz,self.V2.Vz]
        ])
        Sol = Merme.inversa().multiplyM(TerminosIndepes)
        RetX = (Sol.contents[0][0]*R.V.Vx)+R.P0.X
        RetY = (Sol.contents[0][0]*R.V.Vy)+R.P0.Y
        RetZ = (Sol.contents[0][0]*R.V.Vz)+R.P0.Z
        return Point(RetX,RetY,RetZ)
class Matrix:
    def __init__(self,contents_):
        self.contents = deepcopy(contents_)
    def inversa(self):
        det = self.determinante()
        if(det==0):
            return 
        return self.adjunta().traspuesta().multiplyN(1/det)
    def traspuesta(self):
        NewCont = [ [ None for a in self.contents ] for b in self.contents[0] ]
        i = 0
        for row in self.contents:
            j = 0
            for element in row:
                NewCont[j][i]=element
                j = j+1
            i = i+1    
        return Matrix(NewCont)
    def adjunta(self):
        ret = [ [ None for i in self.contents[0] ] for j in self.contents ]
        i = 0
        for row in ret:
            j=0
            for e in row:
                ret[i][j] = self.menor(i,j).determinante()*pow(-1,(i+j))
                j=j+1
            i=i+1
        return Matrix(ret)
    def determinante(self):
        if(len(self.contents)==1):
            return self.contents[0][0]
        ret = 0
        i = 0
        for e in self.contents[0]:
            m = 1
            if i%2==1:
                m = -1
            ret = ret + e*int(self.menor(0,i).determinante() * m)
            i=i+1
        return ret
    def menor(self,x,y):
        NewCont = [ [ None for i in range(len(self.contents[0])-1) ] for j in range(len(self.contents)-1) ]
        i = 0
        a = 0
        for row in NewCont:
            if(i>=x):
                a = 1
            j = 0
            b = 0
            for e in row:
                if(j>=y):
                    b = 1
                NewCont[i][j] = self.contents[i+a][j+b]

                j = j+1

            i = i+1
        return Matrix(NewCont)
    def multiplyN(self,n):
        ret = [ [ None for i in self.contents[0] ] for j in self.contents ]
        i = 0
        for row in ret:
            j=0
            for e in row:
                ret[i][j] = self.contents[i][j]*n
                j=j+1
            i=i+1
        return Matrix(ret)
    def multiplyM(self,M):
        if(len(M.contents)!=len(self.contents[0])):
            return len(M.contents),len(self.contents[0])
        ret = [ [ None for i in M.contents[0] ] for j in self.contents ]

        i = 0
        for row in ret:
            j=0
            for e in row:
                r = 0
                Sl = self.contents[i]
                Sm = M.traspuesta().contents[j]
                k = 0
                for Se in Sl:
                    r = r + Se*Sm[k]
                    k = k+1
                ret[i][j] = r
                j=j+1
            i=i+1


        return Matrix(ret)
    def __str__(self):
        return str(self.contents)
def VectorFromPP(P0,P1):
    return Vector(P0.X-P1.X,P0.Y-P1.Y,P0.Z-P1.Z)
def rayFromPointVector(P,V):
    return Ray(P,V.fixVector(P))
def PlaneFromNormalPoint(Vn,P):
    Nvx,Nvy,Nvz = Vn.ToArray()
    V1 = Vector(0,Nvz,-Nvy)
    V2 = Vector(Nvy,-Nvx,0)
    return Plane(V1,V2,P)
def VectorFromArr(arr):
    return Vector(arr[0],arr[1],arr[2])
def PointFromArr(arr):
    return Point(arr[0],arr[1],arr[2])
def sqrt(a):
    return a**.5

def LaunchRay(P,V,bounces):
    global _EmptySceneData
    R = rayFromPointVector(P,V)
    RayData = []
    TotalShortCut = P
    for RayData in _EmptySceneData:
        RayShortCut = P
        InitialRayData = []
        for Esf in RayData:
            Intersections = Esf.RayIntersection(R,True)
            if(Intersections):
                InitialRayData.append(Esf)
                if(VectorFromPP(P,Intersections[0]).modulo()>VectorFromPP(P,RayShortCut).modulo()):
                    P = Intersections[0]
                
                if(VectorFromPP(P,Intersections[1]).modulo()>VectorFromPP(P,RayShortCut).modulo()):
                    P = Intersections[1]
            else:
                break
        if(VectorFromPP(P,TotalShortCut).modulo()>VectorFromPP(P,RayShortCut).modulo()):
            TotalShortCut = RayShortCut
            RayData = deepcopy(InitialRayData)

    obj = None
    hit = False
    Pos = TotalShortCut
    StepCounter = 0
    while not hit:
        D,TempObj = MinDistanceToScene(Pos)
        if(D>CERO or VectorFromPP(P,Pos).modulo>MaxDistance):
            RayData.append(Sphere(Pos,D.modulo))
            Pos = Pos.transform(V.normalice(D))
            StepCounter +=1
        else:
            hit = True
            obj = TempObj
            _EmptySceneData.append(RayData)
        
    if not hit:
        return Sky
    SurfaceR,SurfaceG,SurfaceB = obj.Color(Pos)
    

    colorR = Sky[0]*SurfaceR
    colorG = Sky[1]*SurfaceG
    colorB = Sky[2]*SurfaceB
    #ir a luces
    for lam in _SceneIlumination:
        V = [0,0,1]

        if(lam.type=="Point"):
            V = VectorFromPP(Pos,lam.Pos).normalice(1)
            intensityR,intensityG,intensityB = lam.color
            hit = False
            ilum = False
            Lpos = Pos.transform(V.normalice(0.1))
            while not hit and not ilum:
                dMater = MinDistanceToScene(Lpos)
                dLight = VectorFromPP(Lpos,lam.Pos).modulo()
                d = min(dMater,dLight)
                Lpos = Lpos.transform(V.normalice(d))

                if dLight<CERO :
                    hit = True
                elif dLight<CERO :
                    ilum = True
                    brightConstant = lam.brightness * math.cos(angle(V,obj.normal(Pos))) * 1/VectorFromPP(Pos,lam.Pos).modulo()
                    colorR = colorR + SurfaceR*intensityR*brightConstant
                    colorG = colorG + SurfaceG*intensityG*brightConstant
                    colorB = colorB + SurfaceB*intensityB*brightConstant
                
                
    #implement ambient Oclusion and clamp
    r = min(colorR*((1/(StepCounter+1)/1000)+1),250)
    g = min(colorG*((1/(StepCounter+1)/1000)+1),250)
    b = min(colorB*((1/(StepCounter+1)/1000)+1),250)
    return (r,g,b)

def angle(v1, v2):
    if(v1.modulo * v2.modulo != 0):
        a = v1.ScalarProduct(v2) / (v1.modulo * v2.modulo)
        a = max(min(a,1),-1)
        return math.acos(a)
    return 0

def bounceVectors(d,n,R):
    #Vdir -( 2 * (Vdir * Vnor )*Vnor)
    
    A = d.ScalarProduct(n)
    B = n.normalice(A*n.modulo*2)

    Center = (d-B).normalice(1-R) + n.normalice(R)
    angle = math.pi*R


    return [Center]

def rotateVAngleXYZ(v,aX,aY,aZ):
    return VectorFromArr(np.dot(rotation_matrix((0,0,1), aZ), np.dot(rotation_matrix((0,1,0), aY), np.dot(rotation_matrix((1,0,0), aX), v.ToArray()))))

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

def MinDistanceToScene(Pos):
    global _SceneContents
    ret = [_SceneContents[0],_SceneContents[0].DistanceTo(Pos)]
    for i,obj in enumerate(_SceneContents):
        if(i>0):
            d = obj.DistanceTo(Pos)
            if(ret[1]<d):
                ret = [obj,d]
    return ret

def Main():

    CameraPos = Point(0,0,0)
    size = (300,300)
    screen = pygame.display.set_mode(size,HWSURFACE|DOUBLEBUF|RESIZABLE)
    pxArr = pygame.PixelArray(screen)
    quit = False
    while not quit:
        StartMillis = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
            elif event.type==pygame.VIDEORESIZE:
                size = event.dict['size']
                screen=pygame.display.set_mode(size,HWSURFACE|DOUBLEBUF|RESIZABLE)
                pxArr = pygame.PixelArray(screen)
                pygame.display.flip()
        
        sideLenght = 0

        zoom = 3

        ScreenSpacePoint = [int(size[0]/2),int(size[1]/2)]


        while sideLenght-1<size[0] or sideLenght-1<size[1]:
            c = 0
            if(sideLenght % 2 == 0):
                c = 1
            else:
                c=-1
            for i in range(sideLenght):
                ScreenSpacePoint[0] += c
                CreateRay(zoom,size,pxArr,CameraPos,ScreenSpacePoint)
            for i in range(sideLenght):
                ScreenSpacePoint[1] += c
                CreateRay(zoom,size,pxArr,CameraPos,ScreenSpacePoint)

            sideLenght +=1

        print("tick")
        EndMilis = time.time()

        print("FPS:"+str(1/(EndMilis-StartMillis)))

        pygame.display.update()
    
    print("Finish Main")

_Trail = 0

def CreateRay(zoom,size,SurfaceArr,CPos,SSPos):
    
    #print(SSPos)
    if SSPos[0]<=size[0]-1 and SSPos[1]<=size[1]-1 and SSPos[0]>=0 and SSPos[1]>=0:
        global _Trail
        _Trail=(_Trail+10)%250
        minSize = min(size)
        V = Vector(1,zoom*SSPos[0]/minSize,zoom*SSPos[1]/minSize)
        SurfaceArr[SSPos[0]][SSPos[1]] = LaunchRay(CPos,V,0)
    


    




Main()

sys.stdout = open("Out.txt", "w")