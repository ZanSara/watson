from flask import render_template, request, jsonify
from app import app, results_code
import json
import requests as req
from PIL import Image
import config as cf
import urllib, io
from app.static.dataset import manage_collections as m

def getBestFashionBlogger(json_data):
    data = json.loads(json_data)
    #number of pixels of the cutted images width
    basewidth = 200
    #array to put all the fb images similar
    fb_array = []
    # load the imgs from the URL
    for i in range(0, len(data)):
        file = io.BytesIO(urllib.request.urlopen(data[i]['url']).read())
        img = Image.open(file)
        # load the parameters of the img
        x = data[i]['x']
        y = data[i]['y']
        w = data[i]['w']
        h = data[i]['h']
        # cut & resize the image
        img_cutted = img.crop((x, y, x + w, y + h))
        wpercent = (basewidth/float(img_cutted.size[0]))
        hsize = int((float(img_cutted.size[1])*float(wpercent)))
        img_resized = img_cutted.resize((basewidth,hsize), Image.ANTIALIAS)
        # save the image
        img_resized.save("temp/out" + str(i) + ".jpg")
        fb_similars = m.getKSimilar("temp/out" + str(i) + ".jpg","fashon_blogger_e4ceff",100)
        for fb in fb_similars:
            fb_array.append(fb)
        
    fb_array.sort()
    fb_array_cumulative = []
    temp=[]
    #Eleviamo gli score al quadrato per penalizzare i bassi punteggi
    #e dare più importanza a quelli più alti
    for i in range(0,len(fb_array)):
        if(i==0):
            temp.append(fb_array[i][0])#append image_file_name
            temp.append(fb_array[i][1]**2)#score
            temp.append(fb_array[i][2])#metadata
        else:
            if (temp[0]==fb_array[i][0]):
                temp[1]+=(fb_array[i][1]**2)#score
            else:
                fb_array_cumulative.append(temp)
                temp=[]
                temp.append(fb_array[i][0])#append image_file_name
                temp.append(fb_array[i][1]**2)#score
                temp.append(fb_array[i][2])#metadata
    fb_array_cumulative.append(temp)
    fb_array_cumulative.sort(key=lambda x: x[1], reverse=True)
    best_fb=fb_array_cumulative[0]
    # COMMENTED FOR CICLE TO PRINT THE LINKS RECEIVED 
    print(json.dumps(data, indent=4))
    return best_fb
