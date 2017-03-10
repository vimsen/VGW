import os, time
from datetime import timedelta
from datetime import datetime
import subprocess
import socket
import numpy
import paho.mqtt.client as mqtt
from subprocess import call, Popen, PIPE, STDOUT

#Static Variables ....
VGWname = "genVGW1"
ActivationDate = "Sep 22 2016 08:12:13"

mqttc = mqtt.Client()
mqttc.connect("94.70.239.217", 1883, 60)

# Return the MAC address of interface
def getMAC(interface):
  try:
    mac = open('/sys/class/net/' + interface + '/address').readline()
    str= mac.replace(':','')
  except:
    mac = "00:00:00:00:00:00"
    str= mac.replace(':','')
  return str[0:12]

mqttc.loop_start()
print ' --------------------------------------------------------------'
print 'Now = ' + str(datetime.now())

# get MAC
myMAC = VGWname + "/" + getMAC("eth0")
print 'MAC = ' + myMAC
mqttc.publish(myMAC+"/VGW/MAC/", "%s" % myMAC, 1, retain=True);

# VGWname
print 'VGWname = ' + VGWname
mqttc.publish(myMAC + "/VGW/name/", "%s" % VGWname, 1, retain=True);

# Activation Date
print 'Activation Date = ' + ActivationDate 
mqttc.publish(myMAC + "/VGW/Activation_Date/", "%s" % ActivationDate, 1, retain=True);

# firmware
firmware = os.popen("/opt/vc/bin/vcgencmd version").read()
print 'Last Firmware Version = ' + firmware.split()[9]
mqttc.publish(myMAC + "/VGW/firmware_version/", "%s" % firmware.split()[9], 1, retain=True);
last_upd = firmware.split()[0] +  ' ' + firmware.split()[1] + ' ' + firmware.split()[2] + ' ' + firmware.split()[3]
print 'Firmware Update = ' + last_upd
mqttc.publish(myMAC + "/VGW/firmware_update/", "%s" % last_upd, 1, retain=True);

#freeRAM
myRAM = os.popen("free -o -h").read()
print 'total RAM = ' + myRAM.split()[7] + ' | ' + 'used RAM = ' + myRAM.split()[8] + ' | ' + 'free RAM = ' + myRAM.split()[9]
mqttc.publish(myMAC + "/VGW/RAM/total/", "%s" % myRAM.split()[7], 1, retain=True);
mqttc.publish(myMAC + "/VGW/RAM/used/", "%s" % myRAM.split()[8], 1, retain=True);
mqttc.publish(myMAC + "/VGW/RAM/free/", "%s" % myRAM.split()[9], 1, retain=True);

#eth0 Global IP
from urllib2 import urlopen
my_Global_IPv4 = urlopen('http://ip.42.pl/raw').read()
print 'eth0 Global IPv4 = ' + my_Global_IPv4
#        eth0IPv4Global = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
#        print 'eth0 Global IPv4 = ' + eth0IPv4Global
mqttc.publish(myMAC + "/VGW/eth0_Global_IPv4/", "%s" % my_Global_IPv4, 1, retain=True);
numbers1 = list(map(int, my_Global_IPv4.split('.')))
eth0_Global_IPv6 = '2002:{:02x}{:02x}:{:02x}{:02x}::'.format(*numbers1)
print "eth0 Global IPv6 = " + eth0_Global_IPv6
mqttc.publish(myMAC + "/VGW/eth0_Global_IPv6/", "%s" % eth0_Global_IPv6, 1, retain=True);

# IPv4 address
#        ip addr show dev eth0 | grep "inet " | cut -d ' ' -f 6  | cut -f 1 -d '/'
#	get_eth0IP  = os.popen("ip addr show dev eth0").read()
cmd1 = 'ip addr show dev eth0'
get_eth0IP = Popen(cmd1, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
output = get_eth0IP.stdout.read()
#	print output
if "Device" in output:
	print "eth0_Local_IPv4 = " + get_eth0IP 
	mqttc.publish(myMAC + "/VGW/eth0_Local_IPv4/", "%s" % output, 1, retain=True);
	mqttc.publish(myMAC + "/VGW/eth0_Local_IPv6/", "%s" % "N/A", 1, retain=True);
else:
	get_eth0IP  = os.popen("ip addr show dev eth0").read()
	eth0IP2 = get_eth0IP.split('inet',1)[1]
	eth0IP = eth0IP2.split('brd',1)[0]
    	print "eth0 Local IPv4 = " + eth0IP
     	mqttc.publish(myMAC + "/VGW/eth0_Local_IPv4/", "%s" % eth0IP, 1, retain=True);
#### translate to IPv6
        realIP = eth0IP.split('/',1)[0] # remove /xx
	numbers0 = list(map(int, realIP.split('.')))
       	eth0_Local_IPv6 = '2002:{:02x}{:02x}:{:02x}{:02x}::'.format(*numbers0)
       	print "eth0 Local IPv6 = " + eth0_Local_IPv6
	mqttc.publish(myMAC + "/VGW/eth0_Local_IPv6/", "%s" % eth0_Local_IPv6, 1, retain=True);

#        get_ppp0IP = os.popen("ip addr show dev ppp0").read()
cmd2 = 'ip addr show dev ppp0'
get_ppp0IP = Popen(cmd2, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
output1 =  get_ppp0IP.stdout.read()
#        print output1
if "Device" in output1:
	print "ppp0 IPv4 = " + output1
	mqttc.publish(myMAC + "/VGW/ppp0_IPv4/", "%s" % output1, 1, retain=True);
        mqttc.publish(myMAC + "/VGW/ppp0_IPv6/", "%s" % "N/A", 1, retain=True);
else:
 	get_ppp0IP = os.popen("ip addr show dev ppp0").read()
	ppp0IP2 = str(get_ppp0IP).split('inet',1)[1]
	ppp0IP = ppp0IP2.split('peer',1)[0]
       	print "ppp0IPv4 = " + ppp0IP
	mqttc.publish(myMAC + "/VGW/ppp0_IPv4/", "%s" % ppp0IP, 1, retain=True);
        numbers2 = list(map(int, ppp0IP.split('.')))
       	ppp0_IPv6 = '2002:{:02x}{:02x}:{:02x}{:02x}::'.format(*numbers2)
       	print "ppp0_IPv6 = "+ ppp0_IPv6
        mqttc.publish(myMAC + "/VGW/ppp0_IPv6/", "%s" % ppp0_IPv6, 1, retain=True);

#       get_tun0IP = os.popen("ip addr show dev tun0").read()
cmd3 = 'ip addr show dev tun0'
get_tun0IP = Popen(cmd3, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
output2 =  get_tun0IP.stdout.read()
#        print output2
if "Device" in output2:
       	print  "tun0 IPv4 = " + output2
	mqttc.publish(myMAC + "/VGW/tun0_IPv4/", "%s" % output2, 1, retain=True);
        mqttc.publish(myMAC + "/VGW/tun0_IPv6/", "%s" % "N/A", 1, retain=True);
else:
	get_tun0IP = os.popen("ip addr show dev tun0").read()
        tun0IP2 = get_tun0IP.split('inet',1)[1]
        tun0IP = tun0IP2.split('peer',1)[0]
        print "tun0_Ipv4 = " + tun0IP
      	mqttc.publish(myMAC + "/VGW/tun0_IPv4/", "%s" % tun0IP, 1, retain=True);
        numbers3 = list(map(int, tun0IP.split('.')))
        tun0_IPv6 = '2002:{:02x}{:02x}:{:02x}{:02x}::'.format(*numbers3)
        print "tun0_IPv6 = " + tun0_IPv6
        mqttc.publish(myMAC + "/VGW/tun0_IPv6/", "%s" % tun0_IPv6, 1, retain=True);

#uptime
with open('/proc/uptime', 'r') as x:
        uptime_seconds = float(x.readline().split()[0])
        uptime_string = str(timedelta(seconds = uptime_seconds))
print 'Uptime = ' + uptime_string
mqttc.publish(myMAC + "/VGW/uptime/", "%s" % uptime_string, 1, retain=True);

#CPUload
f = open('/proc/loadavg', 'r')
CPUloadAll = f.readline()
CPUload = CPUloadAll.split(' ',1)[0]
print "CPUload: " + CPUload
mqttc.publish(myMAC + "/VGW/CPUload/", "%s" % CPUload, 1, retain=True);
#CPUtemp
g = open('/sys/class/thermal/thermal_zone0/temp', 'r')
CPUtempAll = g.readline().split(' ',1)[0]
CPUtemp = float(CPUtempAll)/1000
print 'CPU temp = ' + str(CPUtemp)
mqttc.publish(myMAC + "/VGW/CPUtemp/", "%s" % CPUtemp, 1, retain=True);

#PING
#	ping_response = subprocess.Popen(["/bin/ping", "-c1", "-w100", "8.8.8.8"], stdout=subprocess.PIPE).stdout.read()	
#	print ping_response
hostname = "google.com" #example
response = os.system("ping -c 1 -w2 " + hostname + " > /dev/null 2>&1")
if response == 0:
    print hostname, 'is up!' + '@ ' +  str(datetime.now())
    mqttc.publish(myMAC + "/VGW/LastPing/", "%s" % str(datetime.now()), 1, retain=True);
else:
    print hostname, 'is down!'
	    # REBOOOOOOOOOOT?????

mqttc.loop_stop()
mqttc.disconnect()

