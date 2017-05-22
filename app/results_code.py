import requests as req
from flask import request
import json
from PIL import Image
import config as cf
from dataset import manage_collections as m

def outfit_builder(request):
    # Fake data from /page3
    json_data = request.form['imageArray']
    data = json.loads(json_data)
    print(data)
    outdata = data[0]
    
    url = outdata['url']  # "https://scontent.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/18513116_1737915606223692_336722120291647488_n.jpg"
    response = req.get(url).content  # Questo content e' uno stream binario.
    # Non sapendo come calcolare le dimensioni di un'immagine da uno stream binario
    # per ora lo salvo in un file temporaneo, lo riapro e ne ottengo w e h.
    # Salva l'immagine in un file temporaneo sul server
    with open("temp/outfit.jpg", "wb") as outfit_file:
        binary_image = bytearray(response)
        outfit_file.write(binary_image)
    
    # Cerca l'immagine piu simile
    image=m.getKSimilar("temp/outfit.jpg","fashon_blogger_e4ceff")
    #in image c'e il percorso del fashion blogger piu simile in locale
    
    # Apre l'immagine e ne legge le dimensioni
    full_outfit_image = Image.open("temp/outfit.jpg")
    width, height = full_outfit_image.size
    print("dimension:", width, height)
    
    
    # in futuro avro' piu' liste di ritagli, ricorda!
    items = [
                { 'top':(outdata['y'] / height) * 100, 'left':(outdata['x'] / width) * 100, 'width':(outdata['w'] / width) * 100, 'height':(outdata['h'] / height) * 100 },
            ]
    return (url, items)
