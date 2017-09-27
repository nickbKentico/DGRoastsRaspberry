#!/usr/bin/python2.7
import socket, json, time, requests, locale

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
counter = 1
error = False
project_id = "84ebeafd-cad0-47e5-811a-789df7a43ad0"
locale.setlocale( locale.LC_ALL, "" )
while True:
    internetError = False
    print ("Getting Data From Cloud")
    try:
        response = requests.get("https://deliver.kenticocloud.com/" + project_id + "/items?system.type=coffee")
        print ("got the data")
        cloudItems = response.json()
        with open('CloudDataFull.json','w') as outfile:
            json.dump(cloudItems,outfile)
        print("CLoud Data Retrieved and stored")
    except:
        error = True
        internetError = True
        print("Error Getting Items From Cloud")
        cloudItems = json.loads(open('CloudDataFull.json').read())
    print(cloudItems)
      
    # elements in the "Coffee" content type
    # Coffee Codename: 'coffee'
    # System: 
    #   name                    i['system']['name']
    # Elements: 
    #   coffee_name            i['elements']['coffee_name']['value']
    #   price                   i['elements']['price']['value']
    #   photo[]                 i['elements']['photo']['value'][0]['name']
    #   Promotion               i['elements']['promotion']['value'][0]['name']
    #   short_description       
    #   long_description        
    #   product_status (tax)
    #   farm
    #   country
    #   variety
    #   processing
    #   altitude
    print ("Jumping into a loop of data")
    for i in cloudItems['items']:
        elements = []
        convertedPrice = locale.currency(i['elements']['price']['value'], grouping=True)
        haspromotion = ""
        hasprocessing = ""
        try:
            haspromotion = i['elements']['promotion']['value'][0]['name']
        except:
            error = True
        try:
            hasprocessing = i['elements']['processing']['value'][0]['name']
        except:
            error = True
        elements.append(dict(
            coffee_name = i['elements']['coffee_name']['value'],
            photo = i['elements']['photo']['value'][0]['name'],
            short_description = i['elements']['short_description']['value'],
            farm = i['elements']['farm']['value'],
            country = i['elements']['country']['value'],
            variety = i['elements']['variety']['value'],
            price = convertedPrice,
            promotion = haspromotion,
            processing = hasprocessing,
            wifiError = internetError,
	    ))

        #convertedPrice = locale.currency(i['elements']['price']['value'], grouping=True)
        #elements.append(dict(
        #     price = convertedPrice,
        #     ))
        exisitingJson = json.loads(open('CloudData.json').read())
        print ("I have the item as JSON")
        a, b =json.dumps(elements, sort_keys=True),json.dumps(exisitingJson, sort_keys=True)
        #for i in cloudItems['items']:
                #if a != b:
                 #download image
        print ("I am downloading an image")
        try:
            image = requests.get(i['elements']['photo']['value'][0]['url'])
            with open(i['elements']['photo']['value'][0]['name'],"wb") as f:
                f.write(image.content)
                f.close()
                #End Download Image
        except:
            error = True
        with open('CloudData.json','w') as outfile:
            json.dump(elements,outfile)
        print ("The image is downloaded")
        elements = json.dumps(elements, ensure_ascii=False)
        print(elements)

        #TODO Send Info Over a Socket to the InfoBeamer
        coffeeUpdate = "KenticoCloud/update:%s"

        SendLoad = coffeeUpdate % elements
    
        sock.sendto(SendLoad.encode("utf8"), ('127.0.0.1', 4444))
        print ("The load is sent!")
        counter = counter + 1
        print (counter)
        time.sleep(15)
