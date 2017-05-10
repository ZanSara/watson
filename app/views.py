from flask import render_template
from app import app
from time import sleep

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'User'}  # fake user
    return render_template('helloworld.html',
                           title='Home',
                           user=user)
    

@app.route('/page2')
def page2():
    user = {'nickname': 'User'}  # fake user
    return render_template('page2.html',
                           title='page2',
                           user=user)
@app.route('/page3')
def page3():
    user = {'nickname': 'User'}  # fake user
    # here the idea is to show a loading page while the server compute the oufits and then re-render on 
    # the same page the output page with the outfits
    return render_template('page3.html',
                           title='page3',
                           user=user)

