#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import requests , json 
import microgear.client as microgear
import time 
from datetime import datetime
import logging

#Global variable
result = json.dumps(None)

#connect with line notify

url = 'https://notify-api.line.me/api/notify'
token = 'QWZmYQEy3mchGCPb9VdlyruZq7ZqJsD6D8VFNJyjVkr'
headers = {'Authorization':'Bearer '+ token}
msg ="gu sent this message from line notify"
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
microgear.setalias("Pi")
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect
microgear.subscribe("/mails")
microgear.connect(False)


# Read data from Json
read_file = open("plantInfo.json","r", encoding="utf8")
plantAll = json.load(read_file)



#MAIN FUNCTION

while True:
    
    microgear.chat("PlantyPot_web",str(count))  
    microgear.chat("Plant_Detail",str(result))

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    time.sleep(1)