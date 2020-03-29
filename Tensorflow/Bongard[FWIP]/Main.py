from __future__ import absolute_import, division, print_function, unicode_literals
import random
import copy

# TensorFlow y tf.keras
import tensorflow as tf
import os
from tensorflow import keras
from PIL import Image
import numpy as np

size = 40
#Image.open("ProcesedImages/p234/22.png").resize((size,size),resample=Image.BILINEAR).show()
NRITT = []
dir = os.listdir("ProcesedImages")

def getData():
  ret = []
  for name in dir:
    Side1 = []
    Side2 = []
    for img in os.listdir("ProcesedImages/"+name):
      loadimg = Image.open("ProcesedImages/"+name+"/"+img)
      if(img[0]=="1"):
        Side1.append([i[0]/255 for i in list(loadimg.resize((size, size),resample=Image.BILINEAR).getdata())])
      elif(img[0]=="2"):
        Side2.append([i[0]/255 for i in list(loadimg.resize((size, size),resample=Image.BILINEAR).getdata())])
    problem = [Side1,Side2]
    ret.append(problem)
  
    print("Initializing data bulk {:2.1%}".format(dir.index(name) / len(dir)), end="\r")


  return ret
data = getData()

def getExampleXtrainYtrainCouple():
  randProblem = random.randrange(0,len(os.listdir("ProcesedImages")),1)
  randTeam = random.randrange(0,2,1)
  RandImage1 = random.randrange(0,6,1)
  RandImage2 = random.randrange(0,6,1)
  caseId = str(randProblem)+"-"+str(randTeam)+"-"+str(RandImage1)+"-"+str(RandImage2)
  if caseId in NRITT:
    return getExampleXtrainYtrainCouple()
  else:
    NRITT.append(caseId)
    problem = copy.deepcopy(data[randProblem])
    buff = []
    if(randTeam == 0):
      buff = problem[randTeam][RandImage1]
    else:
      buff = problem[randTeam][RandImage2]

    problem[0].pop(RandImage1)
    problem[1].pop(RandImage2)
    Xside= [x for sublist in[x for sublist in [[buff], problem[0], problem[1]] for x in sublist]for x in sublist]
    Yside= [randTeam*0.99]
    return (Xside,Yside)

#print(getExampleXtrainYtrainCouple())

a=range(len(dir))
train = [getExampleXtrainYtrainCouple() for i in a]
Xtrain = np.asarray([a[0] for a in train])
Ytrain = np.asarray([a[1] for a in train])

#Xtrain = [i[0] for i in [1,[3,4],[5,6],[7,8]]]
#Ytrain = [i[1] for i in ExamplesTrain]
#ExamplesTrain[i][0]
model = tf.keras.models.Sequential([
  tf.keras.layers.Dense(len(Xtrain[0])),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(1, activation='softmax')
])

model.compile(optimizer='adam',
  loss='sparse_categorical_crossentropy',
  metrics=['accuracy'])
print(Ytrain)
model.fit(Xtrain, Ytrain, epochs=50, steps_per_epoch=5)

#model.evaluate(x_test,  y_test, verbose=2)

