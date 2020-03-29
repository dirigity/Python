import wget as wget
import os as os
import shutil

shutil.rmtree("RawImages")
os.mkdir("RawImages")


def getFullSize(s, n, spacer = '0'):
    ret = ''
    while True:
        if (len(ret)+len(str(n))==s):
            return ret+str(n)
        ret = ret + spacer
    
print(getFullSize(3,0))

for i in range(1,334):
    if(i==300):
        continue
    names = ['bongard','doughof','foundal','insana','shanahan','foundal','howells','rispoli','gunnarsson','rispoli','ihde','barenbaum','merse','joon','lewis','foundal','lewis','stepo','fairbanks']
    indexes = [0,101,157,201,233,238,240,245,247,260,261,262,264,281,284,300,301,311,317]
    name = ''
    for j in range(len(indexes)+1):
        print(indexes[j],i)
        if(indexes[j]>i):
            name = names[j-1]
            break

    
    try:
        image_url = 'https://www.foundalis.com/res/bps/'+name+'/p'+str(getFullSize(3,i))+'.gif'
        image_dest = "RawImages/" 
        print(image_url)
        wget.download(image_url,image_dest)
    except:
        image_url = 'https://www.foundalis.com/res/bps/'+name+'/p'+str(getFullSize(3,i))+'.png'
        image_dest = "RawImages/" 
        print(image_url)
        wget.download(image_url,image_dest)


