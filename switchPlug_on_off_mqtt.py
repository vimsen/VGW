# Author: George Lyberopoulos, Jan 2016
# The aim of the script is to subscribe to the username/MACaddress/LDRcommand topic, 
# ... to listen to messages (SwitchName, status) and act accordingly (turn specific plug ON or OFF).


# Imports
import subprocess
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

plugStatus = "-" # initial value
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
def onMessage(client, userdata, msg):
    global plugStatus
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    words = str(msg.payload).split(" ") 
    switchName = words[0]
    plugStatus = words[1]
    print switchName
    print plugStatus
#    print isNotBlank(plugStatus)

    myTopic = 'http://localhost:8888/rest/items/' + switchName
#    print myTopic

#   could be used requests instead of subprocess
    subprocess.call([
       'curl',
       '-XPOST',
       '-H',
       'Content-Type:text/plain',
       myTopic, 
       '-d',
       plugStatus
    ])
    print "Command executed ..." 

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
command_topic = "glimperop/" + myMAC + '/LDRcommand'
print command_topic
retain=True

def onConnect(client, userdata, rc):    #event on connecting
    client.subscribe([(command_topic, 1)])  #subscribe

while True:
    try:
        client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol="MQTTv31")
 #       client.username_pw_set(vhost + ":" + username, password)
        client.on_connect = onConnect
        client.on_message = onMessage
        client.connect(broker, broker_port, keepalive=60, bind_address="") #connect
        client.loop_forever()   #automatically reconnect once loop forever
    except Exception, e:
        #when initialize connection, reconnect on exception
        print "Exception handled, reconnecting...\nDetail:\n%s" % e 
        time.sleep(5)
