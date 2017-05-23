#Four collection have already been created, and they are bound to the api_key
#available in this page. There is no need to re-create them neither to re-load
#images.
#Watson developer cloud available at: https://github.com/watson-developer-cloud/python-sdk/blob/master/watson_developer_cloud/visual_recognition_v3.py

import json
import os
from app.static.dataset import utils
import config as cf
from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV3
import mimetypes

upper_body_id="upper_body_711fdd"
lower_body_id="lower_body_8b6402"
full_body_id="full_body_2ae404"
fashion_blogger_id="fashon_blogger_e4ceff"

#All the function are referred to the collection chosen here below
#folder=join(cf.APP_STATIC, "dataset/collections/fashion_blogger")
folder="../static/img/dataset/collections/fashion_blogger"
this_collection_id=fashion_blogger_id


                
def deleteAllCollections():
    collections=visual_recognition.list_collections()
    for collection in collections["collections"]:
        visual_recognition.delete_collection(collection["collection_id"])
def createAllCollections():
    visual_recognition.create_collection("upper_body")
    visual_recognition.create_collection("lower_body")
    visual_recognition.create_collection("full_body")
    visual_recognition.create_collection("fashon_blogger")
    print(visual_recognition.list_collections())
def addAllImagesFromFolder():
    file_list=os.listdir(folder)
    counter=0
    for file in file_list:
            counter+=1
            print(counter)
            with open(join(folder,file), 'rb') as img: 
                string_array_cutted_images = utils.read_cutted_images()#            
                json_array_cutted_images_list=json.loads(string_array_cutted_images)
                json_array_cutted_images_dict = json_array_cutted_images_list[0]
                try:
                    metadata=json_array_cutted_images_dict[str(file)]
                    visual_recognition.add_image(this_collection_id, img,metadata)               
                except:
                    metadata={"ad":"minchiam"}
                    print(str(file)+" not exists in fashion_cutted.txt")
                    visual_recognition.add_image(this_collection_id, img,metadata)          
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
        
def getKSimilar(src,collection,k=1):
    print("############## SRC {}".format(src))
    with open(src, 'rb') as img: 
        res = visual_recognition.find_similar(this_collection_id,img, 50)#number of returned values
    similars=res["similar_images"]
    best=similars[0]["image_file"]
    
    best = best[cf.APP_ROOT.__len__():]
    best = "..{}".format(best)
    
    print("############## BEST {}".format(best))
    return best
    
#creation object for visual recognition    
visual_recognition = VisualRecognitionV3('2016-05-20', api_key='5becfc0e7dc544e89e36230e9bb58a609280957c')
#deleteAllImagesInCollection()
#addAllImagesFromFolder()

#find similarities
#with open(join(folder,"tt0005.jpg"), 'rb') as img: 
#    res = visual_recognition.find_similar(this_collection_id,img, 50)#number of returned values
#    similars=res["similar_images"]
#    for elem in similars:
#        print (elem['image_file'],elem['score'], elem["metadata"] )
    #visual_recognition.classify(img)

    
