# Four collection have already been created, and they are bound to the api_key
# available in this page. There is no need to re-create them neither to re-load images.
# Watson developer cloud available at: https://github.com/watson-developer-cloud/python-sdk/blob/master/watson_developer_cloud/visual_recognition_v3.py

import json, os, mimetypes
from os.path import join, dirname, normpath

from app.static.dataset import utils
import config as cf
from watson_developer_cloud import VisualRecognitionV3
from random import randint


upper_body_id="upper_body_711fdd"
lower_body_id="lower_body_8b6402"
full_body_id="full_body_2ae404"
fashion_blogger_id = []
fashion_blogger_id.append("fashon_blogger_e4ceff")
fashion_blogger_id.append("fashionBloggers_919987")
##All the function are referred to the collection chosen here below
#folder=join(cf.APP_STATIC, "dataset/collections/fashion_blogger")
folder="app/static/dataset/collections/fashion_blogger"
this_collection_id = fashion_blogger_id[1]

#creation object for visual recognition  
visual_recognition = []
visual_recognition.append(VisualRecognitionV3('2016-05-20', api_key='5becfc0e7dc544e89e36230e9bb58a609280957c'))
visual_recognition.append(VisualRecognitionV3('2016-05-20', api_key='1fd2bd12745641a799e1a1a76a5bccc8a0d85b7d'))

                
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
    print("Number of images added from " + folder + " :")
    for file in file_list:
            counter+=1
            print(counter)
            url=folder+"/"+file
            print(url)
            print(normpath(url))
            with open(url, 'rb') as img:   
                print(img)        
                json_cutted_images =utils.read_cutted_images()             
                try:
                    metadata=json_cutted_images[str(file)]
                    visual_recognition[1].add_image(this_collection_id, img,metadata)               
                except:
                    try:
                        metadata={"error":"Metadata not present"}
                        print(str(file)+" not exists in fashion_cutted.txt")
                        visual_recognition[1].add_image(this_collection_id, img,metadata)  
                    except:          
                        print(str(file)+"create an error, images not added")      
    print(getCollectionLength())
    
    
def getCollectionLength():
    images=visual_recognition[1].list_images(this_collection_id)
    return len(images["images"])
    
    
def deleteAllImagesInCollection():
    images=visual_recognition[1].list_images(this_collection_id)
    counter=0
    for image in images["images"]:
        counter+=1
        print(counter)
        visual_recognition[1].delete_image(this_collection_id,image["image_id"])
    if(len(images["images"])!=0):
        print("collections not empty")      
        

def getKSimilar(src, collection, k=1):
    i = 0    
    #if(collection=="fashon_blogger"):     
    #    i = (randint(0,len(visual_recognition)-1))           
    #    collection = fashion_blogger_id[i]
    #print("--- GETKSIM: src {}".format(src))
    with open(src, 'rb') as img: 
        similars = visual_recognition[i].find_similar(collection,img, k)["similar_images"]    #number of returned values  # collection was this_collection_id
        #print("--- GETKSIM: similar_images: {}".format( [ i['image_id'] for i in similars] ))
        if (k <= 1):
            #print("--- GETKSIM: k equal to 1 or lower")
            best=similars[0]["image_file"]    
            best = best[cf.APP_ROOT.__len__():]
            best = "..{}".format(best)
            #print("--- GETKSIM: best is {}".format(best))
            return best
            
        else:
            #print("--- GETKSIM: k is greater than 1")
            #print( json.dumps( [ (e['image_file'], e['score']) for e in similars[:20]], indent=4 ))
            return similars
    

#deleteAllImagesInCollection()
#addAllImagesFromFolder()

#find similarities
#with open(join(folder,"tt0005.jpg"), 'rb') as img: 
   # res = visual_recognition.find_similar(this_collection_id,img, 50)#number of returned values
    #similars=res["similar_images"]
    #for elem in similars:
     #   print (elem['image_file'],elem['score'], elem["metadata"] )
    #visual_recognition.classify(img)

    
