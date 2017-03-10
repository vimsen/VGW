# Author: George Lyberopoulos, Jan 2016
# get addnewdevice from this topic -> glimperop/MAC-without-:/addnewdevice

# Imports
import pycurl
import time
import json
import unittest
import StringIO
import paho.mqtt.client as mqtt
import urllib2
import datetime
import sys
from sys import argv
import ast

newdevstring="-" # initial value
print newdevstring

# Return the MAC address of interface
def getMAC(interface):
  try:
    mac = open('/sys/class/net/' + interface + '/address').readline()
    str= mac.replace(':','')
  except:
    mac = "00:00:00:00:00:00"
    str= mac.replace(':','')
  return str[0:12]


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global newdevstring
#    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    newdevstring = msg.payload
    print "newdevstring (on_message): " + newdevstring
    print isNotBlank(newdevstring)
    f = open("/home/pi/glimperop.items","a")
    f.write(newdevstring)
#    f.write("\n")
    f.close() 

def isNotBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return True
    #myString is None OR myString is empty or blank
    return False

broker = '94.70.239.217'
broker_port = 1883
myMAC = getMAC("eth0")
print 'MAC = ' + myMAC
newdev_topic = "glimperop/" + myMAC + '/addnewdevice'
print newdev_topic
retain=True

mqttc = mqtt.Client()
mqttc.connect("94.70.239.217", 1883, 60)
mqttc.on_message = on_message
mqttc.subscribe(newdev_topic)
mqttc.loop_start()

# Target
target = '192.168.1.35'
#target = 'arduino.local'

while True:
   mqttc.loop()
