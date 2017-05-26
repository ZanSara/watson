from flask import render_template, request, jsonify
from app import app, results_code
import json
import requests as req
from PIL import Image
import config as cf
import urllib, io
from app.static.dataset import manage_collections as m
import os.path
import string

def getBestFashionBloggerAndClothes(json_data):
    data = json.loads(json_data)
    # number of pixels of the cutted images width
    basewidth = 200
    # array to put all the fb images similar
    fb_array = []
    # load the imgs from the URL
    for i in range(0, len(data)):
        #print(data[i]['url'])
        file = io.BytesIO(urllib.request.urlopen(data[i]['url']).read())
        img = Image.open(file)
        # load the parameters of the img
        x = data[i]['x']
        y = data[i]['y']
        w = data[i]['w']
        h = data[i]['h']
        # cut & resize the image
        img_cutted = img.crop((x, y, x + w, y + h))
        wpercent = (basewidth / float(img_cutted.size[0]))
        hsize = int((float(img_cutted.size[1]) * float(wpercent)))
        img_resized = img_cutted.resize((basewidth, hsize), Image.ANTIALIAS)
        # save the image
        img_resized.save("temp/out" + str(i) + ".jpg")
        fb_similars = m.getKSimilar("temp/out" + str(i) + ".jpg", "fashon_blogger_e4ceff", 100)
        for fb in fb_similars:
            fb_array.append(fb)
        
    fb_array.sort()
    fb_array_cumulative = []
    temp = []
    # Eleviamo gli score al quadrato per penalizzare i bassi punteggi
    # e dare pi√u importanza a quelli piu alti
    for i in range(0, len(fb_array)):
        if(i == 0):
            temp.append(fb_array[i][0])  # append image_file_name
            temp.append(fb_array[i][1] ** 2)  # score
            temp.append(fb_array[i][2])  # metadata
        else:
            if (temp[0] == fb_array[i][0]):
                temp[1] += (fb_array[i][1] ** 2)  # score
            else:
                fb_array_cumulative.append(temp)
                temp = []
                temp.append(fb_array[i][0])  # append image_file_name
                temp.append(fb_array[i][1] ** 2)  # score
                temp.append(fb_array[i][2])  # metadata
    fb_array_cumulative.append(temp)
    fb_array_cumulative.sort(key=lambda x: x[1], reverse=True)
    
    print("@@@@ print cumulative")
    print( json.dumps( [ [i[0], i[1]] for i in fb_array_cumulative[:10]] ) )
    
    best_fb = fb_array_cumulative[0]
    #print("-----------The most similar fb is:-----------")
    #print(best_fb)
    metadata = best_fb[2]
    try:
        # try to use the url obteined from watson (don't work in localhost)
        img2 = Image.open(best_fb[0]) 
    except:
        try:
            # load the path (from here + collections/fashon_blogger/ttXXXXX.jpg)
            position = best_fb[0].find("collections") 
            path = best_fb[0][position:]
            script_dir = os.path.dirname(os.path.abspath(__file__))
            img2 = Image.open(os.path.join(script_dir, path))  
        except:
            print("Image of the most similar fashion blogger not found, used tt0002.jpg by default")
            try:
                img2 = Image.open('/home/s/projects/watson/app/static/dataset/collections/fashion_blogger/tt0002.jpg')
            except:
                # load the path (from here + collections/fashon_blogger/tt0002.jpg)
                path = 'collections/fashion_blogger/tt0002.jpg'
                script_dir = os.path.dirname(os.path.abspath(__file__))
                img2 = Image.open(os.path.join(script_dir, path)) 
    try:
        # it is a upper and down fashion blogger's clothes
        if(metadata['c_w'] == '0'):
            # ritaglio upper
            x = float(metadata['u_x'])
            y = float(metadata['u_y'])
            w = float(metadata['u_w'])
            h = float(metadata['u_h'])
            img_cutted = img2.crop((x, y, x + w, y + h))
            # save the image
            img_cutted.save("temp/upper.jpg")
            upper_similars = m.getKSimilar("temp/upper.jpg", "upper_body_711fdd", 100)
            #print("-----------List of upper similar----------")
            #print(upper_similars)
            # ritaglio down
            x = float(metadata['d_x'])
            y = float(metadata['d_y'])
            w = float(metadata['d_w'])
            h = float(metadata['d_h'])
            img_cutted = img2.crop((x, y, x + w, y + h))
            # save the image
            img_cutted.save("temp/down.jpg")
            down_similars = m.getKSimilar("temp/down.jpg", "lower_body_8b6402", 100)
            #print("-----------List of down similar----------")
            #print(down_similars)
            return {"best_fb":best_fb,
                    "upper": upper_similars,
                    "lower": down_similars}
        else:
            # ritaglio complete
            x = float(metadata['c_x'])
            y = float(metadata['c_y'])
            w = float(metadata['c_w'])
            h = float(metadata['c_h'])
            img_cutted = img2.crop((x, y, x + w, y + h))
            # save the image
            img_cutted.save("temp/complete.jpg")
            complete_similars = m.getKSimilar("temp/complete.jpg", "full_body_2ae404", 100)
            #print("-----------List of complete similar----------")
            #print(complete_similars)         
            return {"best_fb":best_fb,
                    "complete": complete_similars}
    except:
        print("No metadata found, passed center of the image to find similar complete clothes")
        # ritaglio center
        width, height = img2.size
        x = width / 2 - 40
        y = height / 2 - 40
        w = 80
        h = 80
        img_cutted = img2.crop((x, y, x + w, y + h))
        # save the image
        img_cutted.save("temp/center.jpg")
        complete_similars = m.getKSimilar("temp/center.jpg", "full_body_2ae404", 100)
        #print("-----------List of complete similar----------")
        #print(complete_similars)
        return {"best_fb":best_fb,
                "complete": complete_similars}
                
                
                
                
                
                
                
                
                
                
                
                
def funzioneDiProvaSARA(data):
    similars = matchBlogger(data)
    if len(similars) < 1:
        return {'errore': 'Nessun elemento simile trovato'}
    best = similars[0]
    print('### S4P3: the most similar item is {} ({})'.format(best['image_file'], best['score']))
    img = openPath(best['image_file'])
    print('### S4P3: metadata processing\n')
    return matchClothes(img, best['metadata'])
    
 


def matchBlogger(data, basewidth=200):
    """ 
        Dato l'array in arrivo da /page2,
        taglia le immagini e ottiene le risposte da watson
    """
    print('### S4P3: Getting similarities')
    all_similarities = []
    for i, res in enumerate(data):
        x = res['x']
        y = res['y']
        w = res['w']
        h = res['h']
        img_from_url = io.BytesIO( req.get( res['url'] ).content )  # Questo content e' uno stream binario.
                                                                    #file = io.BytesIO(urllib.request.urlopen(data[i]['url']).read())
        with Image.open(img_from_url) as img:
            img_cutted = img.crop( (x, y, x + w, y + h) )
            wpercent = basewidth / img_cutted.size[0]       #wpercent = basewidth / float(img_cutted.size[0])
            hsize = img_cutted.size[1] * wpercent           #hsize = int((float(img_cutted.size[1])*float(wpercent)))
            
            img_resized = img_cutted.resize( (basewidth, int(hsize)), Image.ANTIALIAS)

            img_resized.save("temp/out{}.jpg".format(i))
            
            similar = m.getKSimilar2("temp/out{}.jpg".format(i), "fashon_blogger_e4ceff", 100)
            print('### S4P3: found {} similar\n'.format( len(similar) ))
            all_similarities += similar
            
    print('### S4P3: similars\n')
    print(json.dumps( [ [s['image_file'], s['score']] for s in all_similarities[:10]], indent=4))
    sorted_similars = sorted(all_similarities, key=lambda k: k['score'], reverse=True)
    sorted_and_squared = [ item.update({'score': item['score'] ** 2 }) for item in sorted_similars]
    
    return sorted_and_squared
    



def openPath(path):
    """
        Dato il percorso da aprire, tenta di aprirlo in vari modi.
        Ritorna un oggetto Image
    """
    try:
        img2 = Image.open(path)     # tries to use the url obtained from watson (don't work in localhost)
        
    except:
        print('### S4P3: localhost mode\n')
        
        # load the path (from here + collections/fashon_blogger/ttXXXXX.jpg)
        position = best['image_file'].find("collections") 
        path = best['image_file'][position:]
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        try:
            print('### S4P3: path to image is {}'.format( os.path.join(script_dir, path) ) )
            img2 = Image.open(os.path.join(script_dir, path))
            
        except:
        
            print("### S4P3: Image of the most similar fashion blogger not found, used tt0002.jpg by default")
            try:
                print('### S4P3: online path to default image is {}'.format( "{}{}".format(cf.APP_ROOT, "static/dataset/collections/fashion_blogger/tt0002.jpg") ) )
                img2 = Image.open("{}/{}".format(cf.APP_ROOT, "static/dataset/collections/fashion_blogger/tt0002.jpg") )
            except:
            
                # load the path (from here + collections/fashon_blogger/tt0002.jpg)
                path = 'collections/fashion_blogger/tt0002.jpg'
                print('### S4P3: offline path to default image is {}'.format( os.path.join(script_dir, path) ) )
                img2 = Image.open(os.path.join(script_dir, path))
    
    return img2



def matchClothes(img, metadata):
    """
        Data l'immagine di un fashion blogger e i metadati del ritaglio,
        ritorna un dizionario utile a essere inviato a /results
    """
    try:
        # it is a upper and down fashion blogger's clothes
        if(metadata['c_w'] == '0'):
            # ritaglio upper
            print('### S4P3: crop upper\n')
            x = float(metadata['u_x'])
            y = float(metadata['u_y'])
            w = float(metadata['u_w'])
            h = float(metadata['u_h'])
            img_cutted = img.crop((x, y, x + w, y + h))
            # save the image
            img_cutted.save("temp/upper.jpg")
            upper_similars = m.getKSimilar2("temp/upper.jpg", "upper_body_711fdd", 100)
            
            # ritaglio down
            print('### S4P3: crop lower\n')
            x = float(metadata['d_x'])
            y = float(metadata['d_y'])
            w = float(metadata['d_w'])
            h = float(metadata['d_h'])
            img_cutted = img.crop((x, y, x + w, y + h))
            # save the image
            img_cutted.save("temp/lower.jpg")
            down_similars = m.getKSimilar2("temp/lower.jpg", "lower_body_8b6402", 100)

            output = {"best": best, "upper": upper_similars, "lower": down_similars}
            
        else:
            # ritaglio complete
            print('### S4P3: crop full\n')
            x = float(metadata['c_x'])
            y = float(metadata['c_y'])
            w = float(metadata['c_w'])
            h = float(metadata['c_h'])
            img_cutted = img.crop((x, y, x + w, y + h))
            # save the image
            img_cutted.save("temp/full.jpg")
            full_similars = m.getKSimilar2("temp/full.jpg", "full_body_2ae404", 100)
            output = {"best":best, "full": full_similars}
            
    except:
        print("No metadata found, passed center of the image to find similar complete clothes")
        # ritaglio center
        width, height = img.size
        x = width / 2 - 40
        y = height / 2 - 40
        w = 80
        h = 80
        img_cutted = img.crop((x, y, x + w, y + h))
        # save the image
        img_cutted.save("temp/center.jpg")
        full_similars = m.getKSimilar2("temp/center.jpg", "full_body_2ae404", 100)
        output = {"best":best, "full": full_similars}
        
    return output
