#@app.route('/page_db')
def pagedb():
    json_data=codecs.open("full_body.json", "r",encoding='utf-8', errors='ignore')
    tosend=[]
    for line in json_data:
        info=json.loads(line)
        items=info["result"]["extractorData"]["data"][1]["group"]
        for item in items:
            try:
                link_to_buy=item["Image"][0]["href"]
                tosend.append(link_to_buy)
            except:
                continue
    tosend=json.dumps(tosend)
    return render_template('get_images.html',data=tosend, title='page_db')

def get_id(link):
    index_first=link.rfind("/")
    index_second=link.rfind("@")
    return(link[index_first+1:index_second])
def search(id_data,items):
    for i in range (len(items)):
        item=items[i]
        sku=item["Sku"][0]["text"]
        if (sku==id_data):
            return i
    return -1
def get_list(stream):
    toreturn=[]
    for line in stream:
        toreturn.append(line)
    return toreturn
def writeFile(i,json_count_elem,data,items):
    str_i=str(i+1)
    while(len(str_i)<5):
        str_i="0"+str_i
    try:
        urllib.request.urlretrieve(data[i],r"app\static\new_dataset\temp2\tt"+str_i+".jpg")
        items[json_count_elem]["Image"][0]["name"]="tt"+str_i+".jpg"
    except:
        print("error to write file")
#@app.route('/file', methods=['POST'])
def file():
    towrite=[]
    data = json.loads(request.data)
    #json_new=codecs.open("lower_body_resp.json", "w",encoding='utf-8', errors='ignore')
    #json.dump(data,json_new)
    json_data=codecs.open("full_body.json", "r",encoding='utf-8', errors='ignore')
    json_data=get_list(json_data)
    json_count_line=0
    json_count_elem=0
    line=json_data[json_count_line]
    info=json.loads(line)
    items=info["result"]["extractorData"]["data"][1]["group"]
    for i in range (len(data)):
        if (data[i][-1]!="l"):
            index=data[i].find("pdp-color-big")
            data[i]=data[i][:index]+"pdp-gallery"+data[i][index+13:]
            id_data=get_id(data[i])
            print("LOOk here")
            print(data[i])
            print(items[json_count_elem]["Sku"][0]["text"])
            print(id_data)
            print()
            try:
                if(id_data==items[json_count_elem]["Sku"][0]["text"]):
                    print("----->",data[i],json_count_elem,"<-----")
                    items[json_count_elem]["Image"][0]["src"]=data[i]
                    try:
                        writeFile(i,json_count_elem,data,items)
                    except:
                        continue
                    if(json_count_elem<len(items)-1):
                        json_count_elem+=1
                    else:
                        if(json_count_line>=len(json_data)-1):
                            break
                        json_count_elem=0
                        json_count_line+=1
                        towrite.append(info)
                        line=json_data[json_count_line]
                        info=json.loads(line)
                        items=info["result"]["extractorData"]["data"][1]["group"]
                else:
                    index=search(id_data,items)
                    if (index==-1):
                        if(json_count_line>=len(json_data)-1):
                            break
                        json_count_line+=1
                        towrite.append(info)
                        line=json_data[json_count_line]
                        info=json.loads(line)
                        items=info["result"]["extractorData"]["data"][1]["group"]
                        index=search(id_data,items)
                        if (index==-1):
                            print("error, no changes!")
                        else:
                            print("Changed page, continuing", i)
                            json_count_elem=index  
                            items[json_count_elem]["Image"][0]["src"]=data[i]
                            try:
                                writeFile(i,json_count_elem,data,items)
                            except:
                                continue
                    else:
                        print("One missing")
                        json_count_elem=index
                        if(json_count_elem<len(items)-1):
                            json_count_elem+=1
                        items[json_count_elem]["Image"][0]["src"]=data[i]
                        try:
                            writeFile(i,json_count_elem,data,items)
                        except:
                            continue
            except:
                print("Something went wrong, probably indexes")
                if(json_count_line>=len(json_data)-1):
                    break
                json_count_line+=1
                towrite.append(info)
                line=json_data[json_count_line]
                info=json.loads(line)
                items=info["result"]["extractorData"]["data"][1]["group"]
                json_count_elem=0
                
            
        else:
            try:
                if(json_count_elem<len(items)-1):
                    json_count_elem+=1
                else:
                    if(json_count_line<len(json_data)-1):
                        json_count_elem=0
                        json_count_line+=1
                        towrite.append(info)
                        line=json_data[json_count_line]
                        info=json.loads(line)
                        items=info["result"]["extractorData"]["data"][1]["group"]
                    else:
                        break
            except:
                print("Error with .html files")
    towrite.append(info)
    with open(r"app\static\new_dataset\temp2\new_full_body.json", 'w') as outfile:
        json.dump(towrite, outfile)
    return json.dumps(info)