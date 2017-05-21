from flask import render_template, request, jsonify
from app import app
import json
import requests as req
from PIL import Image
import config as cf
import urllib, io



########## Static files servers (Do not modify) ###############
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)
###############################################################



@app.route('/')
@app.route('/home')
def home():
    return render_template('homepage.html',
                            title='Home',
                            active_navbar_button="home",
                            background_class="home-background", baseLink="http://127.0.0.1:5000/")
                           
@app.route('/about')
def about():
    return render_template('about.html',
                            title='About Us',
                            active_navbar_button="about",
                            background_class="light-background")
    


@app.route('/images')
def images():
    return render_template('images.html',
                                custom_css=["../static/cropper/dist/cropper.css"],
                                custom_js=["../static/cropper/dist/cropper.js", "../static/js/inpage_cropper_code.js"],
                                title='images')
                           
@app.route('/page2')
def page2():
    return render_template('page2.html',
                                custom_css=["../static/cropper/dist/cropper.css"],
                                custom_js=["../static/cropper/dist/cropper.js", "../static/js/inpage_cropper_code.js"],
                           title='Scegli le tue immagini')
                           
                           
@app.route('/page3', methods=['POST'])
def page3():
    
    if request.method == 'POST':
        #number of pixels of the cutted images width
        basewidth = 200
        json_data = request.form['imageArray']
        data = json.loads(json_data)
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
            
        # COMMENTED FOR CICLE TO PRINT THE LINKS RECEIVED 
        print(json.dumps(data, indent=4))
    
        return render_template('page3.html',
                        postdata=json_data,
                        title='Loading...')



@app.route('/results', methods=['POST'])
def results():
    
    if request.method == 'POST':
    
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
        
        # Apre l'immagine e ne legge le dimensioni
        full_outfit_image = Image.open("temp/outfit.jpg")
        width, height = full_outfit_image.size
        print("dimension:", width, height)
        
        # in futuro avro' piu' liste di ritagli, ricorda!
        items = [
                    { 'top':(outdata['y'] / height) * 100, 'left':(outdata['x'] / width) * 100, 'width':(outdata['w'] / width) * 100, 'height':(outdata['h'] / height) * 100 },
                ]
        
        return render_template('results.html',
                                full_outfit=url,
                                items=items,
                                title='Outfit trovato')
