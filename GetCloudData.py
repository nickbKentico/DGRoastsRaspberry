#!/usr/bin/python2.7
import socket, json, time, requests

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
counter = 1
project_id = "dfc80764-b4d6-4554-aa5f-805c3b2dbef1"
while True:
    response = requests.get("https://deliver.kenticocloud.com/" + project_id + "/items?system.type=event")
    #print(response.text)
    cloudItems = response.json()
    print(cloudItems)
    elements = []
   
    print(counter)
    
    for i in cloudItems['items']:
        elements.append(dict(
            title = i['system']['name'],
            overlay = i['elements']['short_description']['value'],
            background = i['elements']['event_image___hi_res']['value'][0]['name'],
	    contactEmail = i['elements']['contact_email']['value'],
	    contactPhone = i['elements']['contact_phone_number']['value'],
	    eventDate = i['elements']['date_of_event']['value'],
            #backgroundColor = i['elements']['background_color']['value'][0]['codename'],
            ))

    exisitingJson = json.loads(open('CloudData.json').read())
    
    a, b =json.dumps(elements, sort_keys=True),json.dumps(exisitingJson, sort_keys=True)
    
    if a != b:
         #download image
        image = requests.get(cloudItems['items'][0]['elements']['event_image___hi_res']['value'][0]['url'])
        with open(cloudItems['items'][0]['elements']['event_image___hi_res']['value'][0]['name'],"wb") as f:
            f.write(image.content)
            f.close()
        #End Download Image
        with open('CloudData.json','w') as outfile:
            json.dump(elements,outfile)
            print(elements)
   # cloudSocket = "KenticoCloud/update:%s"
   # SendLoad = cloudSocket % data
    
   # sock.sendto(SendLoad.encode("utf8"), ('127.0.0.1', 4444))
    counter = counter + 1
    time.sleep(15)
