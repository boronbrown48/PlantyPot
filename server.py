#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import requests , json 
import microgear.client as microgear
import time 
from datetime import datetime
import logging
import Adafruit_ADS1x15
import RPi.GPIO as GPIO
from random import randint

#Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

#GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT) # Red
GPIO.setup(13,GPIO.OUT) # Green
GPIO.setup(15,GPIO.OUT) # Water

#Global variable
result = json.dumps(None)

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
state_l="Low"
state_m="Medium"
state_h="High"
energy = 100
water_time = ''

def SearchData(name):
    data = plantAll[name] 
    return data 

def decreseEnergyDay(x,value):
    type = {
        "Low": 1,
        "Medium": 2,
        "High": 3
    }
    global energy
    status = ''
    if  type[x["Type"]] == 1 :
        if 1000 < value and 13000 > value :
            status = 'Satisfied'
            if energy == 100 :
                energy = energy
            else :
                energy = energy + (x["energy"][0])
        elif 500 < value and 1000 > value :
            status = 'Unsatisfied'
            energy = energy - (x["energy"][1])
            if energy <= 0 :
                energy = 0
        elif value < 500 :
            status = 'Unsatisfied'
            energy = energy + (x["energy"][2])
            if energy <= 0 :
                energy = 0
        else :
            status = 'Unsatisfied'
            energy = energy + (x["energy"][3])
            if energy <= 0 :
                energy = 0
    elif  type[x["Type"]] == 2 :
        if 500 < value and 4000 > value :
            status = 'Satisfied'
            if energy == 100 :
                energy = energy
            else :
                energy = energy + (x["energy"][1])
        elif 4000 < value :
            status = 'Unsatisfied'
            energy = energy + (x["energy"][0])
            if energy <= 0 :
                energy = 0
        elif value < 500 :
            status = 'Unsatisfied'
            energy = energy + (x["energy"][2])
            if energy <= 0 :
                energy = 0
    elif  type[x["Type"]] == 3 :
        if 400 < value and 3000 > value :
            status = 'Satisfied'
            if energy == 100 :
                energy = energy
            else :
                energy = energy + (x["energy"][2])
        elif 3000 < value and 4000 > value :
            status = 'Unsatisfied'
            energy = energy + (x["energy"][1])
            if energy <= 0 :
                energy = 0
        elif 4000 < value :
            status = 'Unsatisfied'
            energy = energy + (x["energy"][0])
            if energy <= 0 :
                energy = 0
        else :
            status = 'Unsatisfied'
            energy = energy + (x["energy"][3])
            if energy <= 0 :
                energy = 0
    Result = {
        "energy" : energy,
        "status" : status,
    }
    return Result

def decreseEnergyNight(x):
    global energy
    energy = energy + (x["energy"][3])
    status = 'Unsatisfied'
    if energy <= 0 :
        energy = 0
    Result = {
        "energy" : energy,
        "status" : status,
    }
    return Result

def checkMoist(x,value):
    time_delay = {
        "100" : 8,
        "90" : 5,
        "80" : 3
    }
    delay = time_delay[str(x["water"])]
    global water_time
    while x["water"] < value+5 and x["water"] > value-5 :
        now = datetime.now()
        water_time = now.strftime('%m/%d/%Y %I:%M%p')
        #Water pump
        GPIO.output(15, GPIO.HIGH)
        Result = {
            "moist"  : value,
            "latestWater" : str(water_time)
        }
        return Result
    GPIO.output(15, GPIO.LOW)
    Result = {
        "moist"  : value,
        "latestWater" : str(water_time)
    }
    return Result

while True:
    #microgear.chat("Plant_Detail",str(result))
    # Read LDR Sensor and Moist sensor
    light = adc.read_adc(0,gain=GAIN)
    moist = adc.read_adc(1,gain=GAIN)
    moist = moist/300
    #plant
    plant = plantAll["plant01"]
    # time
    now = datetime.now()
    current_time = now.strftime("%I:%M%p")
    hour = int(now.strftime("%I")) 
    minute = int(now.strftime("%M")) 
    p_o_a = now.strftime("%p")
    # Check Light
    # Compare time
    if p_o_a in ["PM"] :    
        if (hour > 6 and hour <= 12) :
            res_l = decreseEnergyNight(plant)
        else :
            res_l = decreseEnergyDay(plant,light)
    elif p_o_a in ["AM"] :
        if (hour >= 0 and hour < 6) :
            res_l = decreseEnergyNight(plant)
        else :
            res_l = decreseEnergyDay(plant,light)
    #Test=============================
    #res_l = decreseEnergyDay(plant,light)
    #=================================
    if res_l["status"] in ["Unsatisfied"] :
        GPIO.output(7,GPIO.HIGH)
        GPIO.output(13,GPIO.LOW)
    else :
        GPIO.output(7,GPIO.LOW)
        GPIO.output(13,GPIO.HIGH)
    #Demo
    #if (minute > 10 and minute < 12) :
    #    res = decreseEnergyNight(Test_Cactus)
    #else :
    #    res = decreseEnergyDay(Test_Cactus,3100)
    #Check Moist
    res_m = checkMoist(plant,moist)
    
    # Output
    result = {
        "thai_name" : str(plant["thaiName"]),
        "eng_name" : str(plant["engName"]),
        "energy" : str(res_l["energy"]),
        "status" : str(res_l["status"]),
        "moist"  : str(res_m["moist"]),
        "latestWater" : str(res_m["latestWater"]),
        "img" : str(plant["img"])
    }
    print("Type = ",plant["Type"])
    print("Light = ",light)
    print("moist = ",moist)
    print("result_Light = ",res_l)
    print("result_Moist = ",res_m)
    print("Current Time =", current_time)
    print("Result : ",str(result))
    microgear.chat("PlantyPot_Detail",str(result))
    
    time.sleep(2)


