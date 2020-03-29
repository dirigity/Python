
import copy
import math 

l = 3
players = ["a","b"]
playersIA = [False,True]
tablero = create(l)
#tablero [x][y][h]
main()
def create(l):
    ret = []
    for i in range(l):
        a = []
        for i in range(l):
            b = ["n","n","n"]
            a.append(b)
        ret.append()

    
    return ret

def newTablero(TableroV, x, y, t):
    TableroN = copy.deepcopy(TableroV)
    puesta = False
    for h in range(l):
        if (not puesta) and TableroV[x][y][h]=="n":
            TableroV[x][y][h]=t
            puesta = True

    return TableroN

def Ganador(TableroN):
    for x in range(l):
        for y in range(l):
            for h in range(l):
                r = Linea(TableroN,x,y,h)
                if(r != "n"):
                    return r
    return "n"

def Linea(Tablero,x,y,h):
    v = Tablero[x][y][h]
    if(v =="n"):
        return "n"
    #horx
    c = 0
    for i in range(l):
        if(Tablero[i][y][h]==v):
            c = c+1
    if(c==l):
        return v
    #hory
    c = 0
    for i in range(l):
        if(Tablero[x][i][h]==v):
            c = c+1
    if(c==l):
        return v
    #horh
    c = 0
    for i in range(l):
        if(Tablero[x][y][i]==v):
            c = c+1
    if(c==l):
        return v

    #digPlhx
    c=0
    for i in range(l):
        n = i%l
        if(Tablero[x+n][y][h+n]==v):
            c = c+1
    if(c==l):
        return v

    c=0
    for i in range(l):
        n = i%l
        if(Tablero[x+n][y][h-n]==v):
            c = c+1
    if(c==l):
        return v
    #digPlhy
    c=0
    for i in range(l):
        n = i%l
        if(Tablero[x][y+n][h+n]==v):
            c = c+1
    if(c==l):
        return v
    c=0
    for i in range(l):
        n = i%l
        if(Tablero[x][y+n][h-n]==v):
            c = c+1
    if(c==l):
        return v
    #digPlxy
    c=0
    for i in range(l):
        n = i%l
        if(Tablero[x+n][y+n][h]==v):
            c = c+1
    if(c==l):
        return v
    c=0
    for i in range(l):
        n = i%l
        if(Tablero[x+n][y-n][h]==v):
            c = c+1
    if(c==l):
        return v
    #dePerdidosAlRio
    c=0
    for i in range(l):
        n = i%l
        if(Tablero[x+n][y-n][h+n]==v):
            c = c+1
    if(c==l):
        return v

    c=0
    for i in range(l):
        n = i%l
        if(Tablero[x+n][y-n][h-n]==v):
            c = c+1
    if(c==l):
        return v

    c=0
    for i in range(l):
        n = i%l
        if(Tablero[x+n][y+n][h+n]==v):
            c = c+1
    if(c==l):
        return v

    c=0
    for i in range(l):
        n = i%l
        if(Tablero[x+n][y+n][h-n]==v):
            c = c+1
    if(c==l):
        return v
    return "n"

def newIATablero(OldTs,OldHisM,name,inteligenceLeft):

    HistorialM = []
    for i in range(len(OldTs)):
        OldH = OldHisM[i]
        for x in range(l):
            for y in range(l):
                wipOldH = copy.deepcopy(OldH)
                wipOldH.append([x,y])
                HistorialM.append(wipOldH)
    PosiblesTableros = PosibleTs(OldTs,name)
 
    Perdidas = []
    Ganadas = []
    nextTsIndex = []
    nextTs = []
    nextHist = []

    for i in range(len(PosiblesTableros)):
        if (Ganador(PosiblesTableros[i])!=name):
            Perdidas.append(i)
        elif(Ganador(PosiblesTableros[i]==name)):
            Ganadas.append(i)
        else:
            nextTs.append(PosiblesTableros[i])
            nextHist.append(HistorialM[i])
            nextTsIndex.append(i)
    
    if(len(Ganadas)!=0):
        return ["gotIt",OldHisM[math.floor(Ganadas[0]/math.pow(l,2))][0]]
    else:
        
    ret = []
    
    return 0

def PosibleTs(OldTs,name):
    ret = []
    for i in range(len(OldTs)):
        for x in range(l):
            for y in range(l):
                ret.append(newTablero(OldTs[i],x,y,name))
    return ret

def newUITablero(OldT):
    return 0


def main():
    ganador = "n"
    turno = 0
    while ganador == "n":
        name = players[turno]
        if(playersIA[turno]):
            tablero = newIATablero([tablero],name,10)
        else:
            tablero = newUITablero(tablero);
        

        ganador = Ganador(tablero)
        turno = int((turno + 1)%len(players))
    return
