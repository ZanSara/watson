from flask import render_template, request, jsonify, session, abort, make_response

import json, urllib, io, os
import requests as req
import config as cf


from app import app, results_code, uploader
from app.static.new_dataset import query_watson as q
from app.static.new_dataset import manage_collections as m



########## Static files servers (Do not modify) ###############
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

############## FAKE INSTAGRAM LOGIN ###########################

@app.route('/fake_login_service')
def fake_login_service():
    return '{"pagination":{},"data":[{"id":"1516271018519773447_5443604958","user":{"id":"5443604958","full_name":"Davide Anghileri","profile_picture":"https://scontent.cdninstagram.com/t51.2885-19/s150x150/18013768_1515373448537386_1346263378741428224_a.jpg","username":"davideanghi"},"images":{"thumbnail":{"width":150,"height":150,"url":"https://scontent.cdninstagram.com/t51.2885-15/s150x150/e35/18513116_1737915606223692_336722120291647488_n.jpg"},"low_resolution":{"width":320,"height":320,"url":"https://scontent.cdninstagram.com/t51.2885-15/s320x320/e35/18513116_1737915606223692_336722120291647488_n.jpg"},"standard_resolution":{"width":640,"height":640,"url":"https://scontent.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/18513116_1737915606223692_336722120291647488_n.jpg"}},"created_time":"1494973612","caption":null,"user_has_liked":false,"likes":{"count":0},"tags":[],"filter":"Normal","comments":{"count":0},"type":"image","link":"https://www.instagram.com/p/BUK4HUyF0EHV0i5vSKS4eVpczJEpZ8K2xIjZwI0/","location":null,"attribution":null,"users_in_photo":[]},{"id":"1516270764621640336_5443604958","user":{"id":"5443604958","full_name":"Davide Anghileri","profile_picture":"https://scontent.cdninstagram.com/t51.2885-19/s150x150/18013768_1515373448537386_1346263378741428224_a.jpg","username":"davideanghi"},"images":{"thumbnail":{"width":150,"height":150,"url":"https://scontent.cdninstagram.com/t51.2885-15/s150x150/e35/18443646_677304585795279_134828987745566720_n.jpg"},"low_resolution":{"width":320,"height":320,"url":"https://scontent.cdninstagram.com/t51.2885-15/s320x320/e35/18443646_677304585795279_134828987745566720_n.jpg"},"standard_resolution":{"width":320,"height":320,"url":"https://scontent.cdninstagram.com/t51.2885-15/s320x320/e35/18443646_677304585795279_134828987745566720_n.jpg"}},"created_time":"1494973582","caption":null,"user_has_liked":false,"likes":{"count":0},"tags":[],"filter":"Normal","comments":{"count":0},"type":"image","link":"https://www.instagram.com/p/BUK4DoUlTKQFkLvO6NBZptMx8FKaSFXo-H7H5s0/","location":null,"attribution":null,"users_in_photo":[]},{"id":"1516270630923964506_5443604958","user":{"id":"5443604958","full_name":"Davide Anghileri","profile_picture":"https://scontent.cdninstagram.com/t51.2885-19/s150x150/18013768_1515373448537386_1346263378741428224_a.jpg","username":"davideanghi"},"images":{"thumbnail":{"width":150,"height":150,"url":"https://scontent.cdninstagram.com/t51.2885-15/s150x150/e35/c0.40.320.320/18513257_520920141631134_422573036160417792_n.jpg"},"low_resolution":{"width":320,"height":400,"url":"https://scontent.cdninstagram.com/t51.2885-15/e35/18513257_520920141631134_422573036160417792_n.jpg"},"standard_resolution":{"width":320,"height":400,"url":"https://scontent.cdninstagram.com/t51.2885-15/e35/18513257_520920141631134_422573036160417792_n.jpg"}},"created_time":"1494973566","caption":null,"user_has_liked":false,"likes":{"count":0},"tags":[],"filter":"Normal","comments":{"count":0},"type":"image","link":"https://www.instagram.com/p/BUK4BrzlJBaEhs2UhknpyptSYyNzvDxwMtx0Kw0/","location":null,"attribution":null,"users_in_photo":[]},{"id":"1516270497108975798_5443604958","user":{"id":"5443604958","full_name":"Davide Anghileri","profile_picture":"https://scontent.cdninstagram.com/t51.2885-19/s150x150/18013768_1515373448537386_1346263378741428224_a.jpg","username":"davideanghi"},"images":{"thumbnail":{"width":150,"height":150,"url":"https://scontent.cdninstagram.com/t51.2885-15/s150x150/e35/18580019_436604413371322_3263082458035257344_n.jpg"},"low_resolution":{"width":320,"height":320,"url":"https://scontent.cdninstagram.com/t51.2885-15/s320x320/e35/18580019_436604413371322_3263082458035257344_n.jpg"},"standard_resolution":{"width":640,"height":640,"url":"https://scontent.cdninstagram.com/t51.2885-15/e35/18580019_436604413371322_3263082458035257344_n.jpg"}},"created_time":"1494973550","caption":null,"user_has_liked":false,"likes":{"count":0},"tags":[],"filter":"Normal","comments":{"count":0},"type":"image","link":"https://www.instagram.com/p/BUK3_vLleC2WqD3ve4E-j2EKRI-ih3N6vyqONs0/","location":null,"attribution":null,"users_in_photo":[]},{"id":"1516270236324036376_5443604958","user":{"id":"5443604958","full_name":"Davide Anghileri","profile_picture":"https://scontent.cdninstagram.com/t51.2885-19/s150x150/18013768_1515373448537386_1346263378741428224_a.jpg","username":"davideanghi"},"images":{"thumbnail":{"width":150,"height":150,"url":"https://scontent.cdninstagram.com/t51.2885-15/s150x150/e35/18514125_303163466796621_4427182839095623680_n.jpg"},"low_resolution":{"width":320,"height":320,"url":"https://scontent.cdninstagram.com/t51.2885-15/e35/18514125_303163466796621_4427182839095623680_n.jpg"},"standard_resolution":{"width":320,"height":320,"url":"https://scontent.cdninstagram.com/t51.2885-15/e35/18514125_303163466796621_4427182839095623680_n.jpg"}},"created_time":"1494973519","caption":null,"user_has_liked":false,"likes":{"count":0},"tags":[],"filter":"Normal","comments":{"count":0},"type":"image","link":"https://www.instagram.com/p/BUK378Tl38YG3TE647xrB8MZuJBz7MXw54kfK80/","location":null,"attribution":null,"users_in_photo":[]},{"id":"1512412022666845639_5443604958","user":{"id":"5443604958","full_name":"Davide Anghileri","profile_picture":"https://scontent.cdninstagram.com/t51.2885-19/s150x150/18013768_1515373448537386_1346263378741428224_a.jpg","username":"davideanghi"},"images":{"thumbnail":{"width":150,"height":150,"url":"https://scontent.cdninstagram.com/t51.2885-15/s150x150/e35/18382405_912226935583699_3818473367799857152_n.jpg"},"low_resolution":{"width":320,"height":320,"url":"https://scontent.cdninstagram.com/t51.2885-15/s320x320/e35/18382405_912226935583699_3818473367799857152_n.jpg"},"standard_resolution":{"width":640,"height":640,"url":"https://scontent.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/18382405_912226935583699_3818473367799857152_n.jpg"}},"created_time":"1494513584","caption":null,"user_has_liked":true,"likes":{"count":1},"tags":[],"filter":"Perpetua","comments":{"count":0},"type":"image","link":"https://www.instagram.com/p/BT9Kri1Fl3HUN1taUahSYKrRFR60SSDmwZy1Ug0/","location":null,"attribution":null,"users_in_photo":[]}],"meta":{"code":200}}'


############## ERROR HANDLERS ###########################

@app.errorhandler(400)
def method_not_allowed(e):
    return render_template('500.html',
                            title="Bad Request",
                            background_class="light-background"), 500

@app.errorhandler(401)
def method_not_allowed(e):
    return render_template('403.html',
                            title="Not Allowed!",
                            background_class="light-background"), 401

@app.errorhandler(403)
def method_not_allowed(e):
    return render_template('403.html',
                            title="Not Allowed!",
                            background_class="light-background"), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',
                            title="Not Found!",
                            background_class="light-background"), 404
                            
@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('405.html',
                            title="Not Allowed!",
                            background_class="light-background"), 405
    
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html',
                            title="Internal Error",
                            background_class="light-background"), 500
                            
@app.route('/test<int:code>')
def testcode(code):
    abort(code)
    
###############################################################


@app.route('/')
@app.route('/homeTutorial')
def homeTutorial():
    platform = request.user_agent.platform
    phones = ["iPhone", "android", "blackberry", "Windows Phone"]    
    if (platform in phones) and 'tutorial' not in request.cookies:
        return render_template('homeTutorial.html',
                            title='HomeTutorial',
                            active_navbar_button="home",
                            background_class="home-background")
    return render_template('homepage.html',
                            title='Home',
                            active_navbar_button="home",
                            background_class="home-background")
        
@app.route('/home')
def home():
    resp = make_response(render_template('homepage.html',
                            title='Home',
                            active_navbar_button="home",
                            background_class="home-background"))
    
    resp.set_cookie('tutorial', 'done')
    return resp       

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html',
                            title='Tutorial',
                            active_navbar_button="home",
                            background_class="home-background")
                           
@app.route('/about')
def about():
    return render_template('about.html',
                            title='About Us',
                            active_navbar_button="about",
                            background_class="light-background")
@app.route('/feedback')
def feedback():
    return render_template('questionnaire.html',
                            title='Questionnaire',
                            active_navbar_button="feedback",
                            background_class="light-background")
    
@app.route('/privacy')
def privacy():
    return render_template('privacy.html',
                            title='Privacy Policy',
                            active_navbar_button="privacy",
                            background_class="light-background")
@app.route('/cookie')
def cookie():
    return render_template('cookie-policy.html',
                            title='Cookies Policy',
                            active_navbar_button="cookie",
                            background_class="light-background")
@app.route('/page1')
def page1():
    return render_template('page1.html',
                            custom_css=["../static/css/filepicker.css"],
                            custom_js=["../static/js/inpage_filepicker.js"],
                                title='Carica le tue foto dalla galleria')

                
                           
@app.route('/userPicture')
def userPicture():
    files = os.listdir("{}{}".format(cf.UPLOAD_FILE_PATH, session['logged_in']))
    base_path = "{}{}".format(cf.UPLOAD_WEB_PATH, session['logged_in'])
    
    resdata = [ {'images': {
                    'thumbnail': { 'url': '{}/{}/thumb.png'.format(base_path, f) } ,
                    'standard_resolution': {'url': '{}/{}/full.png'.format(base_path, f) } 
                 } }  for f in files ]
    
    return json.dumps(resdata)

      
                 
@app.route('/page2', methods=['GET', 'POST'])
def page2():
    if request.method == 'POST':
        session['logged_in'] = uploader.upload_photos(request.files)
        return render_template('page2.html',
                                local=1,
                                custom_css=["../static/cropper/dist/cropper.css"],
                                custom_js=["../static/cropper/dist/cropper.js", "../static/js/inpage_cropper.js"],
                                title='Scegli le tue immagini',
                                background_class="light-background")  
                                        
    return render_template('page2.html',
                            local=0,
                            custom_css=["../static/cropper/dist/cropper.css"],
                            custom_js=["../static/cropper/dist/cropper.js", "../static/js/inpage_cropper_code.js"],
                            title='Scegli le tue immagini',
                            background_class="light-background")
                                          




@app.route('/service4page3')
def service4page3():
    
    json_data = request.args.get('data')
    data = json.loads(json_data)
    
    print(json.dumps(data[:10], indent=4))
    
    watson_answer = q.getBestFashionBloggerAndClothes(data)
    # print( json.dumps(watson_answer, indent=4) )
    return json.dumps(watson_answer)
  

@app.route('/images')
def images():
    return render_template('images.html',
                                custom_css=["../static/cropper/dist/cropper.css"],
                                custom_js=["../static/cropper/dist/cropper.js", "../static/js/inpage_cropper_code.js"],
                                title='images')




@app.route('/results', methods=['POST'])
def results():
    if 'logged_in' in session:
        uploader.remove_path(session['logged_in'])
    
    data = json.loads(request.form['imageArray'])
    #print("JSON received by /results: ", json.dumps(data, indent=4))
    
    return render_template('results.html',
                            # jsondata = request.form['imageArray'],
                            fashion=cf.FASHION_BLOGGER_WPATH,
                            lower=cf.LOWER_BODY_WPATH,
                            upper=cf.UPPER_BODY_WPATH,
                            full=cf.FULL_BODY_WPATH,
                            data=data,
                            title='Outfit trovato',
                            background_class="light-background")
                            

