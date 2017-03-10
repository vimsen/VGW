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
hostname='94.70.239.217'
port=1883
client_id="genVGW1_total_energy_only"
auth = {'username':"glimperop", 'password':"glimperop"}

# Setup modbus connection with PM2350 
instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1) # port name, slave address (in decimal)
instrument.serial.parity = minimalmodbus.serial.PARITY_EVEN

# Registers
table = ([	['total_energy',	45166]	])

# Get MAC
myMAC = getMAC("eth0")
# print "My MAC: " + myMAC

while 1:

	for i in xrange(len(table)):
		topic = "glimperop/" + myMAC + "/state/genVGW1_" + table[i][0] + "/state"
		# print topic
		
		try:
			payload = instrument.read_float(table[i][1]-1,3,2)
			# print str(payload)
			publish.single(topic, payload, qos=0, hostname=hostname, port=port, client_id=client_id, auth = auth)
			print "Publishing " + str(payload) + " to topic: " + topic + " ..."

		except Exception as e:
			print "exception"
			log_file=open("log.txt","w")
			log_file.write(str(time.time())+" "+e.__str__())
			log_file.close()
			instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1) # port name, slave address (in decimal)
			instrument.serial.parity = minimalmodbus.serial.PARITY_EVEN	
		
	time.sleep(300)
	print " "	
