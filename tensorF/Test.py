from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
import pygame, sys
from pygame.locals import *
import math    
import numpy as np

import time

millis = lambda: int(round(time.time() * 1000))
np.set_printoptions(threshold=sys.maxsize)
mnist = tf.keras.datasets.mnist

HiresFactor = 3
canvasHires = [[0 for i in range(28*HiresFactor)]for i in range(28*HiresFactor)]
changed = 0
chequed = False
CoordsChanged = []



def centerify(arr):

    ret = [[0 for i in range(len(arr[0]))]for i in range(len(arr))]

    borderBot = 0
    for i,row in enumerate(reversed(arr)):
        v = sum(row)
        if(v != 0):
            borderBot = len(arr)-1-i
            break

    borderTop = 0
    for i,row in enumerate(arr):
        v = sum(row)
        if(v != 0):
            borderTop = i
            break

    l = len(arr)

    h = borderBot-borderTop
    marginh = math.floor((l-h)/2)
    transformY = marginh-borderTop #si es positivo hay que subir la imagen



    for y in range(len(arr)):
        for x in range(len(arr[y])):
            if(y-transformY>=0 and y-transformY<len(arr)):
                local = arr[y-transformY][x]
                ret[y][x] = local
    return ret
def fullRefresh():
    for x,row in enumerate(canvasHires):
        for y,e in enumerate(row):
            CoordsChanged.append([x,y])
def compactify(arr):
    ret = np.zeros((28,28))
    for x,row in enumerate(ret):
        for y,i in enumerate(row):
            for a in range(HiresFactor):
                for b in range(HiresFactor):
                    #print("to:"+str(x) + " " + str(y))
                    #print("from:"+str((HiresFactor*x)+a)+" "+str((HiresFactor*y)+b))
                    #print(arr[(HiresFactor*x)+a][(HiresFactor*y)+b])
                    ret[x][y] = ret[x][y] + arr[(HiresFactor*x)+a][(HiresFactor*y)+b]
                    #print(ret[x][y])
                    #print("---")

            ret[x][y] = ret[x][y]/(HiresFactor**2)
    return ret
def draw(v,Scrx,Scry,l):
    global canvasHires
    x0 = math.floor((Scrx/500)*len(canvasHires[0]))
    y0 = math.floor((Scry/500)*len(canvasHires))
    for x in range((l*2)+1):
        for y in range((l*2)+1):
            if(y0-l+y<len(canvasHires) and x0-l+x<len(canvasHires[0]) and canvasHires[y0-l+y][x0-l+x]!=v):
                canvasHires[y0-l+y][x0-l+x] = v
                CoordsChanged.append([y0-l+y,x0-l+x])
def create_model():

    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),

        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
    return model
def printGrid(arr):
    for row in arr:
        rowT = ""
        for i in row:
            if i < 0.1:
                rowT = rowT + "  "
            elif i < 0.2:
                rowT = rowT + " ."
            elif i < 0.3:
                rowT = rowT + " -"
            elif i < 0.4:
                rowT = rowT + " *"
            elif i < 0.5:
                rowT = rowT + " u"
            elif i < 0.6:
                rowT = rowT + " o"
            elif i < 0.7:
                rowT = rowT + " O"
            elif i < 0.8:
                rowT = rowT + " 0"
            elif i < 0.9:
                rowT = rowT + " #"
            else:
                rowT = rowT + " @"
        print(rowT)
def flip(arr):
    return [[arr[y][x] for y in range(len(row))] for x,row in enumerate(arr)]
def fullCenter(arr,traza,texto):
    if traza:
        print(texto)
    return centerify(flip(centerify(flip(arr))))
def main():
    global canvasHires
    global changed 
    global chequed 
    global CoordsChanged 

    model = create_model()
    model.fit(x_train, y_train, epochs=math.floor(len(x_train)/1875))
    model.evaluate(x_test,  y_test, verbose=2)
    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])


    pygame.init()
    windowSurface = pygame.display.set_mode((500, 500), 0, 32)
    pygame.display.set_caption('OCR')


    while True:
        if((not chequed) and millis()-changed>1000):
            chequed = True
            canvasHires = fullCenter(canvasHires,False,"")
            fullRefresh()
            input = compactify(canvasHires)
            #printGrid(input)

            predictions = probability_model.predict(np.array([input]))
            print(predictions)
            print(str(np.argmax(predictions[0])) + " " + str(predictions[0][np.argmax(predictions[0])]))

        for event in pygame.event.get():
            if event.type==QUIT: pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    windowSurface.fill([0, 0, 0])
                    canvasHires = [[0 for i in range(28*HiresFactor)]for i in range(28*HiresFactor)]
                    changed = millis()
                    chequed = False

        button1, button2, button3 = pygame.mouse.get_pressed()
        MouseX,MouseY = pygame.mouse.get_pos()
        if(button1):
            draw(1,MouseX,MouseY,math.floor(HiresFactor))
            changed = millis()
            chequed = False
        elif(button3):
            draw(0,MouseX,MouseY,math.floor(HiresFactor))
            changed = millis()
            chequed = False

        
        for a in CoordsChanged:
            x = a[0]
            y = a[1]
            p = canvasHires[x][y]
            pygame.draw.rect(windowSurface, (p*255,p*255,p*255), (y*500/len(canvasHires[0]),x*500/len(canvasHires[0]),(500/len(canvasHires[0]))+1,(500/len(canvasHires[0]))+1))
        CoordsChanged = []

        pygame.display.flip()

def ProgressBar(i,t,l,name):
    return "progress of "+ name +" :[" + "#"*math.floor((i/t)*l) + "-"*(l-math.floor((i/t)*l)) + "]("+str(i)+"/"+str(t)+")\r"

print("loading and procesing data:")
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0
x_train = np.array([fullCenter(a,i%500==0,ProgressBar(i,len(x_train),40,"train")) for i,a in enumerate(x_train)])
x_test = np.array([fullCenter(a,i%500==0,ProgressBar(i,len(x_test),40,"test")) for i,a in enumerate(x_test)])
print("DONE!")
main()



