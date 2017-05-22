'''
Created on 21 mag 2017

@author: Antonio
'''
import os
categoryPath="list_category_cloth.txt"
img_categoryPath="list_category_img.txt"
list_bbox="list_bbox.txt"

def binarySearchStr(lista,indice, x):
    i=0
    j=len(lista)-1  
    while(i <= j):
        medio = int((i+j)/2)
        #print(x,lista[medio][indice])
        if (x < lista[medio][indice]):
            j = medio - 1
        elif (x > lista[medio][indice]):
            i = medio + 1
        else:
            return medio
    return -1
def binarySearchInt(lista,indice, x):
    i=0
    j=len(lista)-1  
    while(i <= j):
        medio = int((i+j)/2)
        if (x < int(lista[medio][indice])):
            j = medio - 1
        elif (x > int(lista[medio][indice])):
            i = medio + 1
        else:
            return medio
    return -1
def read(path, offset,bbox=False):
    f= open(path, "r")
    file_list = f.readlines()
    file_list=file_list[offset:]
    file_list=getFields(file_list,bbox)
    return file_list
def getFields(file_list,bbox=False):
    newList=[]
    if( not bbox):
        file_list=[line.split() for line in file_list]
        newList=file_list
    else:
        for line in file_list:
            final=[]
            temp=line.split()
            final.append(temp[0])
            final.append([temp[1],temp[2],temp[3],temp[4]])
            newList.append(final)
    return newList
def addId(file_list):
    for i in range(len(file_list)):
        file_list[i].insert(0,str(i+1))
    return file_list
def getDictionary(file_list):
    dictionary=dict()
    for line in file_list:
        dictionary[line[0]]=line[1]
    return (dictionary)
        
def join(X,Y,listToAppend,iX=0,iY=0,integer=True):
    for i in range(len(X)):
        elem=X[i]
        if (integer):
            index=binarySearchInt(Y,iY,int(elem[iX]))
        else:
            index=binarySearchStr(Y,iY,str(elem[iX]))  
        for i in listToAppend:
            elem.append(Y[index][i])
    return X
def getFinalList():   
    categories=addId(read(categoryPath,2))
    images=read(img_categoryPath,2)
    bbox=(read(list_bbox,2,bbox=True))
    bbox.sort()
    images_categories=join(images,categories,[1,2],1,0)
    images_categories.sort()
    #print(images_categories[:10])
    images_categories_bbox=join(images_categories,bbox,[1],integer=False)
    images_categories_bbox.sort()
    return images_categories_bbox

getFinalList()
