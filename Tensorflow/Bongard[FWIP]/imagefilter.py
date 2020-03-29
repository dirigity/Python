import shutil
import os
import numpy
from PIL import Image

shutil.rmtree("ProcesedImages")
os.mkdir("ProcesedImages")

def GB(x,y,z):
    return (x,y,x+z,y+z)


for filename in os.listdir("RawImages"):
    im = Image.open("RawImages/"+filename).convert('RGB')
    #
    print(filename.split('.')[0])
    dir = "ProcesedImages/"+filename.split('.')[0]
    os.mkdir(dir)

    topPadding = 6
    leftPadding = 8
    internalPadding = 10
    side = 98
    secondLeftPadding = 301

    box11 = GB(leftPadding, topPadding, side)
    box12 = GB(leftPadding, topPadding+(side+internalPadding), side)
    box13 = GB(leftPadding, topPadding+2*(side+internalPadding), side)
    box14 = GB(leftPadding+side+internalPadding, topPadding, side)
    box15 = GB(leftPadding+side+internalPadding, topPadding+(side+internalPadding), side)
    box16 = GB(leftPadding+side+internalPadding, topPadding+2*(side+internalPadding), side)

    box21 =GB(secondLeftPadding, topPadding, side)
    box22 =GB(secondLeftPadding, topPadding+(side+internalPadding), side)
    box23 =GB(secondLeftPadding, topPadding+2*(side+internalPadding), side)
    box24 =GB(secondLeftPadding+side+internalPadding, topPadding, side)
    box25 =GB(secondLeftPadding+side+internalPadding, topPadding+(side+internalPadding), side)
    box26 =GB(secondLeftPadding+side+internalPadding, topPadding+2*(side+internalPadding), side)

    im11 = im.crop(box11)
    im12 = im.crop(box12)
    im13 = im.crop(box13)
    im14 = im.crop(box14)
    im15 = im.crop(box15) 
    im16 = im.crop(box16) 
    im21 = im.crop(box21) 
    im22 = im.crop(box22) 
    im23 = im.crop(box23) 
    im24 = im.crop(box24) 
    im25 = im.crop(box25) 
    im26 = im.crop(box26) 
    
    im11.save(dir+"/11.png")
    im12.save(dir+"/12.png")
    im13.save(dir+"/13.png") 
    im14.save(dir+"/14.png") 
    im15.save(dir+"/15.png") 
    im16.save(dir+"/16.png") 
    im21.save(dir+"/21.png") 
    im22.save(dir+"/22.png") 
    im23.save(dir+"/23.png") 
    im24.save(dir+"/24.png") 
    im25.save(dir+"/25.png") 
    im26.save(dir+"/26.png") 
