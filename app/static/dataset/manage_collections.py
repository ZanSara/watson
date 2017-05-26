# Four collection have already been created, and they are bound to the api_key
# available in this page. There is no need to re-create them neither to re-load images.
# Watson developer cloud available at: https://github.com/watson-developer-cloud/python-sdk/blob/master/watson_developer_cloud/visual_recognition_v3.py

import json, os, mimetypes
from os.path import join, dirname

from app.static.dataset import utils
import config as cf

from watson_developer_cloud import VisualRecognitionV3



upper_body_id="upper_body_711fdd"
lower_body_id="lower_body_8b6402"
full_body_id="full_body_2ae404"
fashion_blogger_id="fashon_blogger_e4ceff"

#All the function are referred to the collection chosen here below
#folder=join(cf.APP_STATIC, "dataset/collections/fashion_blogger")
folder="../static/img/dataset/collections/fashion_blogger"
#this_collection_id = fashion_blogger_id

#creation object for visual recognition    
visual_recognition = VisualRecognitionV3('2016-05-20', api_key='5becfc0e7dc544e89e36230e9bb58a609280957c')


                
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
                json_cutted_images =utils.read_cutted_images()             
                try:
                    metadata=json_cutted_images[str(file)]
                    visual_recognition.add_image(this_collection_id, img,metadata)               
                except:
                    metadata={"error":"Metadata not present"}
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
        print("collections not empty")
        
        
def getKSimilar(src,collection,k=1):
    #print("############## SRC {}".format(src))
    with open(src, 'rb') as img: 
        res = visual_recognition.find_similar(collection,img, k)#number of returned values
    similars=res["similar_images"]
    if(k==1):
        best=similars[0]["image_file"]    
        best = best[cf.APP_ROOT.__len__():]
        best = "..{}".format(best)
        #print("############## BEST {}".format(best))
        return best
    else:
        betters = []
        for elem in similars:
            temp = [elem['image_file'],elem['score'],elem['metadata']]          
            betters.append(temp)
        return betters


def getKSimilar2(src, collection, k=1):
    """ 
    Returns the k most similar elements to src
    
        src:    path of the original image
        k:      n of similar elements to return
        
        return a list of k elements similar to src
    """
    #print("--- GETKSIM: src {}".format(src))
    with open(src, 'rb') as img: 
        similars = visual_recognition.find_similar(collection,img, k)["similar_images"]    #number of returned values  # collection was this_collection_id
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
            #print( json.dumps( [ (e['image_file'], e['score']) for e in similars], indent=4 ))
            return similars
    

#deleteAllImagesInCollection()
#addAllImagesFromFolder()

#find similarities
#with open(join(folder,"tt0005.jpg"), 'rb') as img: 
    #res = visual_recognition.find_similar(this_collection_id,img, 50)#number of returned values
    #similars=res["similar_images"]
    #for elem in similars:
    #    print (elem['image_file'],elem['score'], elem["metadata"] )
    #visual_recognition.classify(img)

    
