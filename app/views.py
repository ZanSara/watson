from flask import render_template, request, jsonify
from app import app, results_code
import json
import requests as req
from PIL import Image
import config as cf
import urllib, io
from app.static.dataset import query_watson as q

#from results_code import outfit_builder



########## Static files servers (Do not modify) ###############
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)
###############################################################

############## FAKE INSTAGRAM LOGIN ###########################

@app.route('/fake_login_service')
def fake_login_service():
    return '{"pagination":{},"data":[{"id":"1516271018519773447_5443604958","user":{"id":"5443604958","full_name":"Davide Anghileri","profile_picture":"https://scontent.cdninstagram.com/t51.2885-19/s150x150/18013768_1515373448537386_1346263378741428224_a.jpg","username":"davideanghi"},"images":{"thumbnail":{"width":150,"height":150,"url":"https://scontent.cdninstagram.com/t51.2885-15/s150x150/e35/18513116_1737915606223692_336722120291647488_n.jpg"},"low_resolution":{"width":320,"height":320,"url":"https://scontent.cdninstagram.com/t51.2885-15/s320x320/e35/18513116_1737915606223692_336722120291647488_n.jpg"},"standard_resolution":{"width":640,"height":640,"url":"https://scontent.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/18513116_1737915606223692_336722120291647488_n.jpg"}},"created_time":"1494973612","caption":null,"user_has_liked":false,"likes":{"count":0},"tags":[],"filter":"Normal","comments":{"count":0},"type":"image","link":"https://www.instagram.com/p/BUK4HUyF0EHV0i5vSKS4eVpczJEpZ8K2xIjZwI0/","location":null,"attribution":null,"users_in_photo":[]},{"id":"1516270764621640336_5443604958","user":{"id":"5443604958","full_name":"Davide Anghileri","profile_picture":"https://scontent.cdninstagram.com/t51.2885-19/s150x150/18013768_1515373448537386_1346263378741428224_a.jpg","username":"davideanghi"},"images":{"thumbnail":{"width":150,"height":150,"url":"https://scontent.cdninstagram.com/t51.2885-15/s150x150/e35/18443646_677304585795279_134828987745566720_n.jpg"},"low_resolution":{"width":320,"height":320,"url":"https://scontent.cdninstagram.com/t51.2885-15/s320x320/e35/18443646_677304585795279_134828987745566720_n.jpg"},"standard_resolution":{"width":320,"height":320,"url":"https://scontent.cdninstagram.com/t51.2885-15/s320x320/e35/18443646_677304585795279_134828987745566720_n.jpg"}},"created_time":"1494973582","caption":null,"user_has_liked":false,"likes":{"count":0},"tags":[],"filter":"Normal","comments":{"count":0},"type":"image","link":"https://www.instagram.com/p/BUK4DoUlTKQFkLvO6NBZptMx8FKaSFXo-H7H5s0/","location":null,"attribution":null,"users_in_photo":[]},{"id":"1516270630923964506_5443604958","user":{"id":"5443604958","full_name":"Davide Anghileri","profile_picture":"https://scontent.cdninstagram.com/t51.2885-19/s150x150/18013768_1515373448537386_1346263378741428224_a.jpg","username":"davideanghi"},"images":{"thumbnail":{"width":150,"height":150,"url":"https://scontent.cdninstagram.com/t51.2885-15/s150x150/e35/c0.40.320.320/18513257_520920141631134_422573036160417792_n.jpg"},"low_resolution":{"width":320,"height":400,"url":"https://scontent.cdninstagram.com/t51.2885-15/e35/18513257_520920141631134_422573036160417792_n.jpg"},"standard_resolution":{"width":320,"height":400,"url":"https://scontent.cdninstagram.com/t51.2885-15/e35/18513257_520920141631134_422573036160417792_n.jpg"}},"created_time":"1494973566","caption":null,"user_has_liked":false,"likes":{"count":0},"tags":[],"filter":"Normal","comments":{"count":0},"type":"image","link":"https://www.instagram.com/p/BUK4BrzlJBaEhs2UhknpyptSYyNzvDxwMtx0Kw0/","location":null,"attribution":null,"users_in_photo":[]},{"id":"1516270497108975798_5443604958","user":{"id":"5443604958","full_name":"Davide Anghileri","profile_picture":"https://scontent.cdninstagram.com/t51.2885-19/s150x150/18013768_1515373448537386_1346263378741428224_a.jpg","username":"davideanghi"},"images":{"thumbnail":{"width":150,"height":150,"url":"https://scontent.cdninstagram.com/t51.2885-15/s150x150/e35/18580019_436604413371322_3263082458035257344_n.jpg"},"low_resolution":{"width":320,"height":320,"url":"https://scontent.cdninstagram.com/t51.2885-15/s320x320/e35/18580019_436604413371322_3263082458035257344_n.jpg"},"standard_resolution":{"width":640,"height":640,"url":"https://scontent.cdninstagram.com/t51.2885-15/e35/18580019_436604413371322_3263082458035257344_n.jpg"}},"created_time":"1494973550","caption":null,"user_has_liked":false,"likes":{"count":0},"tags":[],"filter":"Normal","comments":{"count":0},"type":"image","link":"https://www.instagram.com/p/BUK3_vLleC2WqD3ve4E-j2EKRI-ih3N6vyqONs0/","location":null,"attribution":null,"users_in_photo":[]},{"id":"1516270236324036376_5443604958","user":{"id":"5443604958","full_name":"Davide Anghileri","profile_picture":"https://scontent.cdninstagram.com/t51.2885-19/s150x150/18013768_1515373448537386_1346263378741428224_a.jpg","username":"davideanghi"},"images":{"thumbnail":{"width":150,"height":150,"url":"https://scontent.cdninstagram.com/t51.2885-15/s150x150/e35/18514125_303163466796621_4427182839095623680_n.jpg"},"low_resolution":{"width":320,"height":320,"url":"https://scontent.cdninstagram.com/t51.2885-15/e35/18514125_303163466796621_4427182839095623680_n.jpg"},"standard_resolution":{"width":320,"height":320,"url":"https://scontent.cdninstagram.com/t51.2885-15/e35/18514125_303163466796621_4427182839095623680_n.jpg"}},"created_time":"1494973519","caption":null,"user_has_liked":false,"likes":{"count":0},"tags":[],"filter":"Normal","comments":{"count":0},"type":"image","link":"https://www.instagram.com/p/BUK378Tl38YG3TE647xrB8MZuJBz7MXw54kfK80/","location":null,"attribution":null,"users_in_photo":[]},{"id":"1512412022666845639_5443604958","user":{"id":"5443604958","full_name":"Davide Anghileri","profile_picture":"https://scontent.cdninstagram.com/t51.2885-19/s150x150/18013768_1515373448537386_1346263378741428224_a.jpg","username":"davideanghi"},"images":{"thumbnail":{"width":150,"height":150,"url":"https://scontent.cdninstagram.com/t51.2885-15/s150x150/e35/18382405_912226935583699_3818473367799857152_n.jpg"},"low_resolution":{"width":320,"height":320,"url":"https://scontent.cdninstagram.com/t51.2885-15/s320x320/e35/18382405_912226935583699_3818473367799857152_n.jpg"},"standard_resolution":{"width":640,"height":640,"url":"https://scontent.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/18382405_912226935583699_3818473367799857152_n.jpg"}},"created_time":"1494513584","caption":null,"user_has_liked":true,"likes":{"count":1},"tags":[],"filter":"Perpetua","comments":{"count":0},"type":"image","link":"https://www.instagram.com/p/BT9Kri1Fl3HUN1taUahSYKrRFR60SSDmwZy1Ug0/","location":null,"attribution":null,"users_in_photo":[]}],"meta":{"code":200}}'



###############################################################



@app.route('/')
@app.route('/home')
def home():
    return render_template('homepage.html',
                            title='Home',
                            active_navbar_button="home",
                            background_class="home-background")
                           
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
    return render_template('page3.html',
                        title='Loading...')
    

@app.route('/service4page3')
def page4():
    
    if request.method == 'POST':
        json_data = request.form['imageArray']
        bestFB=q.getBestFashionBlogger(json_data)
        print(bestFB)
        return json_data



@app.route('/results', methods=['POST'])
def results():
    
    if request.method == 'POST':
        url = results_code.outfit_builder(request)
        
        clothes_type =[
                        {'code': 'full_body', 'name': 'Full Body', 'images': ["../static/dataset/collections/full_body/img_00000000119.jpg", "../static/dataset/collections/full_body/img_00000000140.jpg"] },
                        {'code': 'upper_body', 'name': 'Upper Body', 'images': ["../static/dataset/collections/upper_body/img_00000000238.jpg", "../static/dataset/collections/upper_body/img_00000000361.jpg", "../static/dataset/collections/upper_body/img_00000000397.jpg"] },
                        {'code': 'lower_body', 'name': 'Lower Body', 'images': ["../static/dataset/collections/lower_body/img_00000000501.jpg", "../static/dataset/collections/lower_body/img_00000001111.jpg"] }
                      ] 
        
        return render_template('results.html',
                                full_outfit=url,
                                full_body = [1],
                                upper_body = [1],
                                lower_body = [1],
                                clothes_type = clothes_type,
                                title='Outfit trovato')
