from copy import deepcopy
import math as m1
from PIL import Image
import numpy as np

class Point:
    def __init__(self,X_,Y_,Z_):
        self.X = X_
        self.Y = Y_
        self.Z = Z_
    def __add__(self,P):
        return Point(P.X+self.X,P.Y+self.Y,P.Z+self.Z)
    def __sub__(self,P):
        return Point(-P.X+self.X,-P.Y+self.Y,-P.Z+self.Z)
    def __str__(self):
        return "P:[X:"+str(self.X)+",Y:"+str(self.Y)+",Z:"+str(self.Z)+"]"

class Vector:
    def __init__(self,X_,Y_,Z_):
        self.Vx = X_
        self.Vy = Y_
        self.Vz = Z_
    def fixVector(self,P):
        return Point(self.Vx+P.X,self.Vy+P.Y,self.Vz+P.Z)
    def __add__(self,V):
        return Point(V.Vx+self.Vx,V.Vy+self.Vy,V.Vz+self.Vz)
    def __str__(self):
        return "V:[X:"+str(self.Vx)+",Y:"+str(self.Vy)+",Z:"+str(self.Vz)+"]"
    def modulo(self):
        return m1.sqrt(pow(self.Vx,2)+pow(self.Vy,2)+pow(self.Vz,2))
    #def ScalarProduct(Self, V)
    #def VectorialProduct(Self, V)

class Rect:
    def __init__(self,P1_,P2_):
        self.P0 = P1_
        self.V = Vector((P2_-P1_).X,(P2_-P1_).Y,(P2_-P1_).Z)
    def ContainsP(self,P):
        l = ((P.X-self.P0.X)/self.V.Vx)
        return P.Y == self.P0.Y+self.V.Vy*l & P.Z == self.P0.Z+self.V.Vz*l
    def MotherPlane(self):
        return Plane(self.V,Vector(0,0,1),self.P0)

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

class Tri:
    def __init__(self,P1_,P2_,P3_):
        self.P1 = P1_
        self.P2 = P2_
        self.P3 = P3_
        self.plane = PlaneFromPPP(P3_,P1_,P2_)
    def perimeter(self):
        return VectorFromPP(self.P1,self.P2).modulo()+VectorFromPP(self.P1,self.P3).modulo()+VectorFromPP(self.P3,self.P2).modulo()
    def area(self):
        s = self.perimeter()/2
        a = VectorFromPP(self.P1,self.P2).modulo()
        b = VectorFromPP(self.P3,self.P2).modulo()
        c = VectorFromPP(self.P1,self.P3).modulo()
        return m1.sqrt(s*(s-a)*(s-b)*(s-c))
    def Intersect(self,R):
        try:
            P = self.plane.RIntersect(R)
        except:
            return "NO"
        #print(P,Tri(P,self.P1,self.P2).area() + Tri(P,self.P3,self.P2).area() + Tri(P,self.P3,self.P2).area(),self.area())
        if(Tri(P,self.P1,self.P2).area() + Tri(P,self.P3,self.P2).area() + Tri(P,self.P3,self.P2).area() > self.area()):
            return "NO"
        return P

def VectorFromPP(P0,P1):
    return Vector(P0.X-P1.X,P0.Y-P1.Y,P0.Z-P1.Z)
   
def PlaneFromPPP(P0,P1,P2):
    return Plane(VectorFromPP(P0,P1),VectorFromPP(P0,P2),P0)
   
#r = Rect(Point(1,1,3),Point(2,2,2))
#t = Tri(Point(0,0,0),Point(0,-10,0),Point(10,0,0))
#print(t.Intersect(r))
faces = []    

def main():
    vertex = []
    print("Loading Start")
    lineList = [line.rstrip('\n') for line in open("OBJ.obj")]
    for line in lineList:
        if(line[0:2]=="v "):
            points = line[2:].split(' ')
            vertex.append(Point(float(points[0]),float(points[0]),float(points[0])))
    for line in lineList:
        if(line[0:2]=="f "):
            points = line[2:].split(' ')
            faces.append(Tri(vertex[int(points[0].split('/')[0])-1],vertex[int(points[1].split('/')[0])-1],vertex[int(points[2].split('/')[0])-1]))
    print("Loading Done")
    render()

def Ray(x,y,z,angleX,angleY,remaningBounces):
    poscamara = Point(x,y,z)
    posdriver = Point(x+m1.cos(angleX),y+m1.sin(angleX),z+m1.sin(angleY))
    ray = Rect(poscamara,posdriver)
    posibilities = []
    for face in faces:
        calc = face.Intersect(ray)
        if(calc!="NO"):
            posibilities.append(face,calc)

    while len(posibilities)>1:
        if(VectorFromPP(posibilities[0][0],poscamara).modulo()>VectorFromPP(posibilities[1][0],poscamara).modulo()):
            posibilities.pop(0)
        else:
            posibilities.pop(1)



    if(remaningBounces == 0):
        if(len(posibilities)==0):
            return [0,0,0]
        return getcolor(posibilities[0][1],posibilities[0][0])
    else:
        NewAngleX=0
        NewAngleY=0
        return Ray(posibilities[0][1].X,posibilities[0][1].Y,posibilities[0][1].Z,NewAngleX,NewAngleY,remaningBounces-1)
    


def render():
    w,h = 100,100
    x,y,z = 10,10,10
    angleX0,angleXF=0,2*m1.pi
    angleY0,angleYF=0,2*m1.pi
    data = [ [ None for a in range(w) ] for b in range(h) ]


    columnN = 0
    for column in data:
        elementN = 0
        for element in column:
            angleX = (angleXF-angleX0)*(elementN/len(column))+angleX0
            angleY = (angleYF-angleY0)*(columnN/len(data))+angleY0
            data[columnN][elementN]=Ray(x,y,z,angleX,angleY,0)
            elementN = elementN+1
        columnN = columnN+1

    img = Image.fromarray(np.asarray(data,dtype=np.uint8), 'RGB' )
    img.save('render.png')
    img.show()


if __name__ == '__main__':
    main()