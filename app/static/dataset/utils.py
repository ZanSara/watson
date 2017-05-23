'''
Created on 21 mag 2017

@author: Antonio
'''
import os
import config as cf

categoryPath = "{}/dataset/list_category_cloth.txt".format(cf.APP_STATIC)
img_categoryPath = "{}/dataset/list_category_img.txt".format(cf.APP_STATIC)
list_bbox = "{}/dataset/list_bbox.txt".format(cf.APP_STATIC)

import math
import json

def read_cutted_images():
    a = []
    b = list(open("{}/dataset/fashion_cutted.txt".format(cf.APP_STATIC)))
    for line in b:
        x = line.split("{")
        y = x[1].split(":")
        z1 = y[1].split(",")
        z2 = y[2].split(",")
        z3 = y[3].split(",")
        z4 = y[4].split(",")
        y = x[2].split(":")
        z5 = y[1].split(",")
        z6 = y[2].split(",")
        z7 = y[3].split(",")
        z8 = y[4].split(",")
        y = x[3].split(":")
        z9 = y[1].split(",")
        z10 = y[2].split(",")
        z11 = y[3].split(",")
        z12 = y[4].split(",")
        y = x[4].split(":")
        z13 = y[1].split(",")
        z14 = y[2].split(",")
        z15 = y[3].split(",")
        z16 = y[4].split(",")
        z1 = str(round(float(z1[0])))
        z2 = str(round(float(z2[0])))
        z3 = str(round(float(z3[0])))
        z4 = str(round(float(z4[0])))
        z5 = str(round(float(z5[0])))
        z6 = str(round(float(z6[0])))
        z7 = str(round(float(z7[0])))
        z8 = str(round(float(z8[0])))
        z9 = str(round(float(z9[0])))
        z10 = str(round(float(z10[0])))
        z11 = str(round(float(z11[0])))
        z12 = str(round(float(z12[0])))
        z13 = str(round(float(z13[0])))
        z14 = str(round(float(z14[0])))
        z15 = str(round(float(z15[0])))
        z16 = str(round(float(z16[0])))

        a.append(str(x[0] + " " + z1 + " " + z2 + " " + z3 + " " + z4 + " " + z5 + " " + z6 + " " + z7 + " " + z8 + " " + z9 + " " + z10 + " " + z11 + " " + z12 + " " + z13 + " " + z14 + " " + z15 + " " + z16))

    content = [x.strip().split(' ') for x in a]
    all_string = []
    all_json = []
    for k in range(0, len(content)):
        dict_line = {
            str(content[k][0]):{
            "fb_x":content[k][1],
            "fb_y":content[k][2],
            "fb_w":content[k][3],
            "fb_h":content[k][4],
            "c_x":content[k][5],
            "c_y":content[k][6],
            "c_w":content[k][7],
            "c_h":content[k][8],
            "u_x":content[k][9],
            "u_y":content[k][10],
            "u_w":content[k][11],
            "u_h":content[k][12],
            "d_x": content[k][13],
            "d_y": content[k][14],
            "d_w": content[k][15],
            "d_h": content[k][16]}
            }
        string_line = json.dumps(dict_line)
        all_string.append(string_line)
        json_line = json.loads(string_line)
        all_json.append(json_line)
    return json.dumps(all_json)

def binarySearchStr(lista, indice, x):
    i = 0
    j = len(lista) - 1  
    while(i <= j):
        medio = int((i + j) / 2)
        # print(x,lista[medio][indice])
        if (x < lista[medio][indice]):
            j = medio - 1
        elif (x > lista[medio][indice]):
            i = medio + 1
        else:
            return medio
    return -1
def binarySearchInt(lista, indice, x):
    i = 0
    j = len(lista) - 1  
    while(i <= j):
        medio = int((i + j) / 2)
        if (x < int(lista[medio][indice])):
            j = medio - 1
        elif (x > int(lista[medio][indice])):
            i = medio + 1
        else:
            return medio
    return -1
def read(path, offset, bbox=False):
    f = open(path, "r")
    file_list = f.readlines()
    file_list = file_list[offset:]
    file_list = getFields(file_list, bbox)
    return file_list
def getFields(file_list, bbox=False):
    newList = []
    if(not bbox):
        file_list = [line.split() for line in file_list]
        newList = file_list
    else:
        for line in file_list:
            final = []
            temp = line.split()
            final.append(temp[0])
            final.append([temp[1], temp[2], temp[3], temp[4]])
            newList.append(final)
    return newList
def addId(file_list):
    for i in range(len(file_list)):
        file_list[i].insert(0, str(i + 1))
    return file_list
def getDictionary(file_list):
    dictionary = dict()
    for line in file_list:
        dictionary[line[0]] = line[1]
    return (dictionary)
        
def join(X, Y, listToAppend, iX=0, iY=0, integer=True):
    for i in range(len(X)):
        elem = X[i]
        if (integer):
            index = binarySearchInt(Y, iY, int(elem[iX]))
        else:
            index = binarySearchStr(Y, iY, str(elem[iX]))  
        for i in listToAppend:
            elem.append(Y[index][i])
    return X
    
def getFinalList():   
    categories = addId(read(categoryPath, 2))
    images = read(img_categoryPath, 2)
    bbox = (read(list_bbox, 2, bbox=True))
    bbox.sort()
    images_categories = join(images, categories, [1, 2], 1, 0)
    images_categories.sort()
    # print(images_categories[:10])
    images_categories_bbox = join(images_categories, bbox, [1], integer=False)
    images_categories_bbox.sort()
    return images_categories_bbox

#getFinalList()
