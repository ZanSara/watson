

import json
import os
from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV3
import mimetypes

upper_body_id="upper_body_711fdd"
lower_body_id="lower_body_8b6402"
full_body_id="full_body_2ae404"
folder=join("..","temp","collections","full_body")
this_collection_id=full_body_id


def deleteAllCollections():
    collections=visual_recognition.list_collections()
    for collection in collections["collections"]:
        visual_recognition.delete_collection(collection["collection_id"])
def createAllCollections():
    visual_recognition.create_collection("upper_body")
    visual_recognition.create_collection("lower_body")
    visual_recognition.create_collection("full_body")
    print(visual_recognition.list_collections())
def addAllImagesInFolder():
    counter=0
    file_list=os.listdir(folder)
    for file in file_list:
        counter+=1
        print(counter)
        with open(join(folder,file), 'rb') as img: 
            visual_recognition.add_image(this_collection_id, img)
    print(getCollectionLength())
def getCollectionLength():
    images=visual_recognition.list_images(this_collection_id)
    return len(images["images"])
def deleteAllImagesInCollection():
    images=visual_recognition.list_images(this_collection_id)
    counter=0
    for image in images["images"]:
        counter+=1
        print(counter)
        visual_recognition.delete_image(this_collection_id,image["image_id"])
    if(len(images["images"])!=0):
        print("error")
#creation object for visual recognition    
visual_recognition = VisualRecognitionV3('2016-05-20', api_key='5becfc0e7dc544e89e36230e9bb58a609280957c')

#creation of image object from path
addAllImagesInFolder()
#deleteAllImagesInCollection()

#find similarities
with open(join(folder,"img_00000000110.jpg"), 'rb') as img: 
    res = visual_recognition.find_similar(this_collection_id,img, 50)#number of returned values
    similars=res["similar_images"]
    for elem in similars:
        print (elem['image_file'],elem['score'] )
    #visual_recognition.classify(img)
    
