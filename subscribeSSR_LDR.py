# Author: George Lyberopoulos, Jan 2016
# sudo apt-get install python-pycurl
# get COMAMNDS from this topic -> sedini/MAC-without-:/LDRcommand

# Imports
#import pycurl
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
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
# GPIO 4 (Phase 1)
GPIO.setup(4, GPIO.OUT) 
# GPIO XX (Phase 2)

# GPIO XXX (Phase 3)


plugStatus = "-"
switchName = "-" 

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
    global plugStatus
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
#    command = msg.payload
#    print "(on_message) -  command: " + command + "  topic = " + msg.topic
    words = str(msg.payload).split(" ")
    switchName = words[0]
    plugStatus = words[1]
    print switchName
    print plugStatus

    if (plugStatus == 'ON'):
       GPIO.output(4,1)
       print "Phase1 = ON"
    else:
       GPIO.output(4,0)
       print "Phase1 = OFF"


broker = '94.70.239.217'
broker_port = 1883
myMAC = getMAC("eth0")
print 'MAC = ' + myMAC
Phase1_command = "sedini/" + myMAC + '/LDRcommand'
print Phase1_command
retain=True

mqttc = mqtt.Client()
mqttc.connect("94.70.239.217", 1883, 60)
mqttc.on_message = on_message
mqttc.subscribe(Phase1_command)
#mqttc.loop_start()
mqttc.loop_forever()

#while True:
#   mqttc.loop()

