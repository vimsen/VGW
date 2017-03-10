# Author: George Lyberopoulos, Jan 2016
# sudo apt-get install python-pycurl

# get howOften from this topic -> glimperop/MAC-without-:/id000000000001/command

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

howOften="60" # initial value
print howOften

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
    global howOften
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    howOften = msg.payload
    print "howOften (on_message): " + howOften

broker = '94.70.239.217'
broker_port = 1883
myMAC = getMAC("eth0")
print 'MAC = ' + myMAC
temp_topic = "glimperop/" + myMAC + '/id000000000009/rest_temp_LR'
humi_topic = "glimperop/" + myMAC + '/id000000000009/rest_humi_LR'
power_topic = "glimperop/" + myMAC + '/id000000000009/rest_power_LR'
rate_topic = "glimperop/" + myMAC + '/id000000000009/command'
print rate_topic
retain=True

mqttc = mqtt.Client()
mqttc.connect("94.70.239.217", 1883, 60)
mqttc.on_message = on_message
mqttc.subscribe(rate_topic)
mqttc.loop_start()

# Target
target = '192.168.1.125'
#target = 'arduino.local'

# Function to make cURL call
def curl_call(target, command):
  buf = StringIO.StringIO()
  c = pycurl.Curl()
  c.setopt(c.URL, target + command)
  c.setopt(c.WRITEFUNCTION, buf.write)
  c.perform()
  c.close()
  return buf.getvalue()

def executeGet():

   answer = curl_call(target,"/temperature")
#    print answer
   words = answer.split(",")
   temp = words[0].split(":")
   temp1 = temp[1].replace(" ", "")
   print temp1    
   mqttc.publish(temp_topic, "%s" % temp1, 1, retain=False);

   answer = curl_call(target,"/humidity")
#    print answer;
   words = answer.split(",")
   humi = words[0].split(":")
   humi1 = humi[1].replace(" ", "")
   print humi1
   mqttc.publish(humi_topic,"%s" % humi1, 1, retain=False);

   answer = curl_call(target,"/power")
#    print answer;
   words = answer.split(",")
   power = words[0].split(":")
   power1 = power[1].replace(" ", "")
   print power1
   mqttc.publish(power_topic,"%s" % power1, 1, retain=False);

#   print "--- in executeGet() ---"
#   print howOften
   print "in executeGet() -> " + howOften
#   print "--------------------"
   time.sleep(ast.literal_eval(howOften))

while True:
   executeGet()
   mqttc.loop()

