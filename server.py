#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import requests , json 
import microgear.client as microgear
import time 
from datetime import datetime
import logging
import random
#Global variable
result = json.dumps(None)

#connect with line notify

url = 'https://notify-api.line.me/api/notify'
token = 'QWZmYQEy3mchGCPb9VdlyruZq7ZqJsD6D8VFNJyjVkr'
headers = {'Authorization':'Bearer '+ token}
#msg ="gu sent this message from line notify"
#response = requests.post(url, headers=headers, data = {'message':msg}) #command for sending message to line


#connect with NETPIE
appid = "PlantyPot"
gearkey = "PFq6FAxQcaBr6ec"
gearsecret =  "GwFmcGEEQfAmAXXexCbmIUCCI"
microgear.create(gearkey,gearsecret,appid,{'debugmode': True})
def connection():
    logging.info("Now I am connected with netpie")

def subscription(topic,message):
    logging.info(topic+" "+message)
    global result
    msg = message.split("'")
    result = SearchData(msg[1])

def disconnect():
    logging.debug("disconnect is work")

microgear.setalias("Pi2")
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect
microgear.subscribe("/mails")
microgear.connect(True)



#MAIN FUNCTION

while True:

    #microgear.chat("PlantyPot_web",str(count))  
    valueObject = {
        "thaiName" : "thai",
        "plantCurrentMoist" : random.randint(0,100),
        "lastestWatering" : "13:00 13/05/21",
        "plantCurrentLight" : random.randint(0,100),
        "plantEnergy" : random.randint(0,100),
    }
    microgear.chat("Plant_Detail",str(valueObject))
    #count=count+1
    #print(count)

    time.sleep(1)