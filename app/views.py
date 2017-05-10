from flask import render_template
from app import app


########## Static files servers (Do not modify) ###############
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)
###############################################################


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'User'}  # fake user
    return render_template('helloworld.html',
                           title='Home',
                           user=user)

@app.route('/home')
def home():
    user = {'nickname': 'User'}  # fake user
    return render_template('home.html',
                           title='Home',
                           user=user)
