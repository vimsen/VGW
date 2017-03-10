import paho.mqtt.publish as publish
import minimalmodbus
import time
import json

# Return the MAC address of interface
def getMAC(interface):
  try:
    mac = open('/sys/class/net/' + interface + '/address').readline()
    str = mac.replace(':','')
  except:
    mac = "00:00:00:00:00:00"
    str = mac.replace(':','')
  return str[0:12]
  
# Setup MQTT
port=1883
client_id="genVGW1_all_measurements"
hostname='94.70.239.217'
auth = {'username':"glimperop", 'password':"glimperop"}

# Setup modbus connection with PM2350 
instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1) # port name, slave address (in decimal)
instrument.serial.parity = minimalmodbus.serial.PARITY_EVEN

# Registers
table = ([	['power_phaseA',	3054]	,\
			['power_phaseB',	3056]	,\
			['power_phaseC',	3058]	,\
			['total_power',		3060]	,\
			['energy_phaseA',	45184]	,\
			['energy_phaseB',	45186]	,\
			['energy_phaseC',	45188]	,\
#			['total_energy',	45166]	,\
			['temperature',		3132]	])

# Get MAC
myMAC = getMAC("eth0")
# print "My MAC: " + myMAC
topic_array=[]
for i in xrange(len(table)):
	topic="glimperop/" + myMAC + "/state/genVGW1_" + table[i][0] + "/state"
	topic_array.append(topic)
# print topic_array

#msgs=[]

while 1:
	msgs = []
	for i in xrange(len(table)):
		try:
			payload = instrument.read_float(table[i][1]-1,3,2)
			if (i<=4) and (payload <0.0001) :
				payload=0
			# print str(payload)
			# publish.single(topic, payload, qos=0, hostname=hostname, port=port, client_id=client_id, auth = auth)
			print "Publishing " + str(payload) + " to topic: " + topic + " ..."
			msgs.append((topic_array[i], payload, 0, False))
		except Exception as e:
			print "exception" + e.__str__() 
			log_file=open("log.txt","w")
			log_file.write(str(time.time())+" "+e.__str__())
			log_file.close()
			instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1) # port name, slave address (in decimal)
			instrument.serial.parity = minimalmodbus.serial.PARITY_EVEN	
	
	publish.multiple(msgs, hostname=hostname, port=port, client_id=client_id)
	time.sleep(10)
	print " "		
