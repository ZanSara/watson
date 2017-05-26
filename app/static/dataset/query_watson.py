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

def getBestFashionBloggerAndClothes(data):
    similars = matchBlogger(data)
    if len(similars) < 1:
        return {'errore': 'Nessun elemento simile trovato'}
    best = similars[0]
    print('### S4P3: the most similar item is {} ({})'.format(best['image_file'], best['score']))
    img = openPath(best['image_file'])
    print('### S4P3: metadata processing\n')
    return matchClothes(img, best)
    
 


def matchBlogger(data, basewidth=200):
    """ 
        Dato l'array in arrivo da /page2,
        taglia le immagini e ottiene le risposte da watson
    """
    print('### matchBlogger: Getting similarities')
    allsim = []
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
            
            similar = m.getKSimilar("temp/out{}.jpg".format(i), "fashon_blogger_e4ceff", 100)
            print('### matchBlogger: found {} similar\n'.format( len(similar) ))
            allsim += similar
            
    #print('### matchBlogger: similars\n')
    #print(json.dumps( [ [s['image_file'], s['score']] for s in allsim[:10]], indent=4))
    #print( [ [s['image_file'], s['score']] for s in allsim[:10]] )
    
    # Eleviamo gli score al quadrato per penalizzare i bassi punteggi
    # e dare piu' importanza a quelli piu alti
    for item in allsim:
        item['score'] = item['score']**2
    sortedsim = sorted(allsim, key=lambda k: k['score'], reverse=True)
    
    return sortedsim
    



def openPath(path):
    """
        Dato il percorso da aprire, tenta di aprirlo in vari modi.
        Ritorna un oggetto Image
    """
    try:
        img2 = Image.open(path)     # tries to use the url obtained from watson (don't work in localhost)
        
    except:
        print('### openPath: localhost mode\n')
        
        # load the path (from here + collections/fashon_blogger/ttXXXXX.jpg)
        position = best['image_file'].find("collections") 
        path = best['image_file'][position:]
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        try:
            print('### openPath: path to image is {}'.format( os.path.join(script_dir, path) ) )
            img2 = Image.open(os.path.join(script_dir, path))
            
        except:
        
            print("### openPath: Image of the most similar fashion blogger not found, used tt0002.jpg by default")
            try:
                print('### openPath: online path to default image is {}'.format( "{}{}".format(cf.APP_ROOT, "static/dataset/collections/fashion_blogger/tt0002.jpg") ) )
                img2 = Image.open("{}/{}".format(cf.APP_ROOT, "static/dataset/collections/fashion_blogger/tt0002.jpg") )
            except:
            
                # load the path (from here + collections/fashon_blogger/tt0002.jpg)
                path = 'collections/fashion_blogger/tt0002.jpg'
                print('### openPath: offline path to default image is {}'.format( os.path.join(script_dir, path) ) )
                img2 = Image.open(os.path.join(script_dir, path))
    
    return img2



def matchClothes(img, best, n_items=10):
    """
        Data l'immagine di un fashion blogger e i metadati del ritaglio,
        ritorna un dizionario utile a essere inviato a /results
    """
    metadata = best['metadata']
    try:
        # it is a upper and down fashion blogger's clothes
        if(metadata['c_w'] == '0'):
            # ritaglio upper
            print('### matchClothes: crop upper')
            x = float(metadata['u_x'])
            y = float(metadata['u_y'])
            w = float(metadata['u_w'])
            h = float(metadata['u_h'])
            img_cutted = img.crop((x, y, x + w, y + h))
            # save the image
            img_cutted.save("temp/upper.jpg")
            upper_similars = m.getKSimilar("temp/upper.jpg", "upper_body_711fdd", n_items)
            
            # ritaglio down
            print('### matchClothes: crop lower')
            x = float(metadata['d_x'])
            y = float(metadata['d_y'])
            w = float(metadata['d_w'])
            h = float(metadata['d_h'])
            img_cutted = img.crop((x, y, x + w, y + h))
            # save the image
            img_cutted.save("temp/lower.jpg")
            down_similars = m.getKSimilar("temp/lower.jpg", "lower_body_8b6402", n_items)

            output = {"best": best, "upper": upper_similars, "lower": down_similars}
            
        else:
            # ritaglio complete
            print('### matchClothes: crop full')
            x = float(metadata['c_x'])
            y = float(metadata['c_y'])
            w = float(metadata['c_w'])
            h = float(metadata['c_h'])
            img_cutted = img.crop((x, y, x + w, y + h))
            # save the image
            img_cutted.save("temp/full.jpg")
            full_similars = m.getKSimilar("temp/full.jpg", "full_body_2ae404", n_items)
            output = {"best":best, "full": full_similars}
            
    except:
        print("### matchClothes: No metadata found, passed center of the image to find similar complete clothes")
        # ritaglio center
        width, height = img.size
        x = width / 2 - 40
        y = height / 2 - 40
        w = 80
        h = 80
        img_cutted = img.crop((x, y, x + w, y + h))
        # save the image
        img_cutted.save("temp/center.jpg")
        full_similars = m.getKSimilar("temp/center.jpg", "full_body_2ae404", n_items)
        output = {"best":best, "full": full_similars}
        
    return output
