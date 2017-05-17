from flask import render_template, request
from app import app
import config as cf


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
                           title='Scegli le tue immagini')
                           
                           
@app.route('/page3', methods=['POST'])
def page3():
    # here the idea is to show a loading page while the server compute the oufits and then re-render on 
    # the same page the output page with the outfits
    if request.method == 'POST':
        return render_template('page3.html',
                                postdata=request.form,
                                title='Loading...')


