'''
Created on 21 mag 2017

@author: Antonio
'''
import utils as u
import os
from shutil import copyfile
from PIL import Image
import os.path
import math
import time

global code1
global code2
global code3
global zeros
global basewidth
def init():
    global code1
    global code2
    global code3
    global zeros
    global basewidth
    basewidth=200
    code1=0
    code2=0
    code3=0
    zeros="0000000000"
def copiaFile(src,dst,info):
    x1=int(info[0])
    y1=int(info[1])
    x2=int(info[2])
    y2=int(info[3])
    img = Image.open(src)
    img_resized=cut(img,x1,y1,x2,y2)
    img_resized.save(dst)
def cut(img,x1,y1,x2,y2):
    img_cutted = img.crop((x1, y1, x2, y2))
    wpercent = (basewidth/float(img_cutted.size[0]))
    hsize = int((float(img_cutted.size[1])*float(wpercent)))
    img_resized = img_cutted.resize((basewidth,hsize), Image.ANTIALIAS)
    return img_resized
def getName(category):
    global code1
    global code2
    global code3
    global zeros
    if category==1:
        code1+=1
        prefix=10-int(math.log10(code1+1))
        toReturn=zeros[:prefix]+str(code1)
    else:
        if category==2:
            code2+=1
            prefix=10-int(math.log10(code2+1))
            toReturn=zeros[:prefix]+str(code2)
        else:
            code3+=1
            prefix=10-int(math.log10(code3+1))
            toReturn=zeros[:prefix]+str(code3)
    return ("img_"+toReturn+".jpg")

init() 
start_time = int(round(time.time()))
print("Started Program "+time.strftime("%H:%M:%S"))
index=0
info=u.getFinalList()
counter=0
for root, dirs, files in os.walk('img'):
     for file in files:
        with open(os.path.join(root, file), "r") as auto:
            counter+=1
            print(counter)
            name=root[4:]+"/"+file
            src= os.path.join("img",root[4:], file)
            dest=os.path.join(info[index][3],getName(info[index][3]))
            if (name>info[index][0][4:]):
                while(name!=info[index][0][4:]):
                    index+=1
                copiaFile(src,dest,info[index][4])
                index+=1
            else:
                if (name<info[index][0][4:]):
                    continue
                else:
                    copiaFile(src,dest,info[index][4])
                    index+=1
print (time.strftime("%H:%M:%S"))
print("Finished in "+str( int(round(time.time()))-start_time)+" seconds")
print("Code1: "+str(code1))
print("Code2: "+str(code2))
print("Code3: "+str(code3))
