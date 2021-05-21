#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import requests 
import microgear.client as microgear
import time
import logging

#connect with line notify

url = 'https://notify-api.line.me/api/notify'
token = 'QWZmYQEy3mchGCPb9VdlyruZq7ZqJsD6D8VFNJyjVkr'
headers = {'Authorization':'Bearer '+ token}
msg ="gu sent this message from line notify"
response = requests.post(url, headers=headers, data = {'message':msg}) #command for sending message to line



#connect with NETPIE
appid = "PlantyPot"
gearkey = "PFq6FAxQcaBr6ec"
gearsecret =  "GwFmcGEEQfAmAXXexCbmIUCCI"
microgear.create(gearkey,gearsecret,appid,{'debugmode': True})
def connection():
    logging.info("Now I am connected with netpie")
def subscription(topic,message):
    logging.info(topic+" "+message)
def disconnect():
    logging.debug("disconnect is work")
microgear.setalias("Pi")
microgear.on_connect = connection
microgear.on_message = subscription
microgear.on_disconnect = disconnect
microgear.subscribe("/mails")
microgear.connect(False)

#MAIN FUNCTION
count=0


while True:
    microgear.chat("PlantyPot_web",str(count))
    microgear.chat("Plant_Detail",str(count))
    count=count+1
    print(count)
    time.sleep(1)