from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'User'}  # fake user
    return render_template('helloworld.html',
                           title='Home',
                           user=user)
