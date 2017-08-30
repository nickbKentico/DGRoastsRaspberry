#!/usr/bin/python2.7
import socket, json, time, requests

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
counter = 1
project_id = "dfc80764-b4d6-4554-aa5f-805c3b2dbef1"
while True:
    print "Getting Data From Cloud"
    response = requests.get("https://deliver.kenticocloud.com/" + project_id + "/items?system.type=coffee")
    print "got the data"
    cloudItems = response.json()
    #print(cloudItems)
      
    # elements in the "Coffee" content type
    # Coffee Codename: 'coffee'
    # System: 
    #   name                    i['system']['name']
    # Elements: 
    #   product_name            i['elements']['product_name']['value']
    #   price                   i['elements']['price']['value']
    #   image[]                 i['elements']['image']['value'][0]['name']
    #   short_description       
    #   long_description        
    #   product_status (tax)
    #   farm
    #   country
    #   variety
    #   processing
    #   altitude
    print "Jumping into a loop of data"
    for i in cloudItems['items']:
        elements = []
        elements.append(dict(
            product_name = i['elements']['product_name']['value'],
            price = i['elements']['price']['value'],
            image = i['elements']['image']['value'][0]['name'],
            short_description = i['elements']['short_description']['value'],
            #long_description = i['elements']['long_description']['value'],
           # product_status (tax)
            farm = i['elements']['farm']['value'],
            country = i['elements']['country']['value'],
            #variety = i['elements']['variety']['value'],
            #processing = i['elements']['processing']['value'],
            #altitude = i['elements']['altitude']['value'],
	    ))

        exisitingJson = json.loads(open('CloudData.json').read())
        print "I have the item as JSON"
        a, b =json.dumps(elements, sort_keys=True),json.dumps(exisitingJson, sort_keys=True)
        #for i in cloudItems['items']:
                #if a != b:
                 #download image
        print "I am downloading an image"
        image = requests.get(i['elements']['image']['value'][0]['url'])
        with open(i['elements']['image']['value'][0]['name'],"wb") as f:
            f.write(image.content)
            f.close()
                #End Download Image
        with open('CloudData.json','w') as outfile:
            json.dump(elements,outfile)
        print "The image is downloaded"
        elements = json.dumps(elements, ensure_ascii=False)
        print(elements)

        #TODO Send Info Over a Socket to the InfoBeamer
        coffeeUpdate = "KenticoCloud/update:%s"

        SendLoad = coffeeUpdate % elements
    
        sock.sendto(SendLoad.encode("utf8"), ('127.0.0.1', 4444))
        print "The load is sent!"
        counter = counter + 1
        print counter
        time.sleep(15)
