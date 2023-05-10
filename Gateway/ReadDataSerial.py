import sys
from Adafruit_IO import MQTTClient
import numpy as np
import random
import time
from collections import Counter
import base64
import cv2 as cv
import serial.tools.list_ports
from Adafruit_IO import Client, Feed

from simpleAI import *
from SpeechToText import *

AIO_FEED_IDs = ['publish-temp', 'publish-humid', 'led-button', 'pump-button']
AIO_USERNAME = 'huy_nglq'
AIO_KEY = 'aio_QrhN15m18uegdjbJRlj7kGyh2OWH'
AIO_DATA = Client(username = AIO_USERNAME, key = AIO_KEY)

# Ket noi voi Adafruit-IO
def connected(client):
    print("Ket noi thanh cong ...")
    #client.subscribe(AIO_FEED_ID)
    for topic in AIO_FEED_IDs:
      client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)
def message(client , AIO_FEED_ID , payload):
    print("Nhan du lieu: "+ payload + ", Feed ID: " + AIO_FEED_ID)
    if AIO_FEED_ID == 'led-button':
        if payload == "OFF":
            writeData("1")
        else:
            writeData("2")
    if AIO_FEED_ID == 'pump-button':
        if payload == "OFF":
            writeData("3")
        else:
            writeData("4")


# Xu ly ve serial
def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    comPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        print(strPort)
        if "USB Serial" in strPort:
            splitPort = strPort.split(" ")
            comPort = (splitPort[0])
    return comPort

if getPort()!= "None":
    ser = serial.Serial(port=getPort(), baudrate=115200)
    print(ser)
mess = ""

def processData(client, data):
    data = data.replace("!","")
    data = data.replace("#","")
    splitData = data.split(":")
    if splitData[1] == "T":
        client.publish("Publish temp", splitData[2])
    elif splitData[1] == "H":
        client.publish("Publish humid", splitData[2])

mess = ""
def readSerial(client):
    bytesToRead = ser.inWaiting()
    if(bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(client, mess[start:end + 1])
            if(end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

def writeData(data):
    ser.write(str(data).encode('utf-8'))

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

counter_ai = 0
while True:
    # readSerial(client)

    counter_ai = counter_ai - 1
    if counter_ai <= 0 :
        counter_ai = 1
        try:
            ai_result = image_detector()
            print("Publish AI Output: ", ai_result)
            client.publish("mask-status", ai_result)
        except:
            print("Error in AI scanning")

    speech_result = speech_detector()
    print(speech_result)
    if speech_result != None:
        if "type" in speech_result and "command" in speech_result:
            if speech_result["type"] == "publish" :
                client.publish(speech_result["feed"], speech_result["command"])
        if "type" in speech_result and "get" in speech_result:
            if "feed" in speech_result:
                currentData = AIO_DATA.receive(speech_result["feed"]).value
                print("The current " + speech_result["get"] + " is : " + currentData)

    time.sleep(5)