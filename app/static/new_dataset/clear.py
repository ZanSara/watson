'''
Created on 05 giu 2017

@author: Antonio
'''

import json
import codecs
json_data = codecs.open("new_lower.json", "r", encoding='utf-8', errors='ignore')
tot=0
towrite=[]
new_items=[]
for line in json_data:
    info = json.loads(line)
    for i in range (len(info)):
        items = info[i]["result"]["extractorData"]["data"][1]["group"]
        new_items=[]
        for a in range(len(items)):
            item=items[a]
            try:
                img_src = item["Image"][0]["src"]
                description = item["Image"][0]["alt"]
                link_to_buy = item["Image"][0]["href"]
                name=item["Image"][0]["name"]
                price = item["Price"][0]["text"]
                sku = item["Sku"][0]["text"]
                print
                print("img_src: ", img_src)
                print("description: ", description)
                print("price: ", price)
                print("link to buy: ", link_to_buy)
                print("sku: ", sku)
                print("name: ", name)
                new_items.append(item)
            except:
                continue
        towrite.append(new_items)
out = codecs.open("lower_body.json", "w", encoding='utf-8', errors='ignore')
json.dump(towrite,out)