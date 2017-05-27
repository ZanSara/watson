import os, random, shutil
from PIL import Image
import config as cf


def upload_photos(f):
    #if not session.get('logged_in',None):
    num = int(round(random.uniform(0, 1), 5) * 100000)
    os.makedirs("{}{}".format(cf.UPLOAD_FILE_PATH, num ))    
    
    for i in range(len(f)-1):
        el = f["images{}".format(i)]
        elpath = "{}{}/file-{}".format(cf.UPLOAD_FILE_PATH, num, i)
        if not os.path.exists(elpath):
            os.makedirs(elpath)
        el.save( "{}/full.png".format( elpath ) )
        
        # Crea un thumbnail
        size = 150, 150
        im = Image.open( "{}/full.png".format( elpath) )
        im.thumbnail(size, Image.ANTIALIAS)
        thumb = Image.new('RGBA', size, (255, 255, 255, 0))
        thumb.paste( im, (int((size[0] - im.size[0]) / 2), int((size[1] - im.size[1]) / 2)) )
        thumb.save( "{}/thumb.png".format( elpath ) )
        
    return num # for views.py to save it in session['logged_in']
    
    
    
    
def remove_path(number):
    #cancella le immagini caricate dall' utente
    try:
        path_to_delete = "{}{}".format( cf.UPLOAD_FILE_PATH, number )
        shutil.rmtree(path_to_delete)
        os.remove(path_to_delete)
    except:
        print('### uploader.remove_path: error while deleting user folder n {}'.format( number ) )
    
