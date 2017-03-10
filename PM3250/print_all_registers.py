#!/usr/bin/env python
import minimalmodbus
#minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True
print(minimalmodbus._getDiagnosticString())
#print(minimalmodbus.BAUDRATE)

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1) # port name, slave address (in decimal)
instrument.serial.parity = minimalmodbus.serial.PARITY_EVEN
#instrument.mode = minimalmodbus.MODE_RTU
#instrument.serial.baudrate = 9600
#instrument.serial.baudrate = 19200 #default
#instrument.serial.baudrate = 38400
#instrument.serial.timeout = 1
instrument.debug = True
#print "Serial Settings: %s" % (instrument)

print instrument

#TODO Add exception, see EM... files

###########################
## Read System Registers ##
###########################

## Read Meter Name - UTF8
print "Meter Name:\t" + instrument.read_string(30-1,20)
## Read Meter Model - UTF8
print "Meter Model:\t" + instrument.read_string(50-1,20)
## Read Manufacturer - UTF8
print "Manufacturer:\t" + instrument.read_string(70-1,20)
## Read Serial number  - UInt32 
print "Serial Number:\t" + str(instrument.read_long(130-1))

#TODO: Date of Manufacturer

## Read Hardware Revision - UTF8 
print "Serial Number:\t" + instrument.read_string(135-1,5)
## Present Firmware Version (DLF format): X.Y.ZTT - UInt16
print "Present Firmware Version:\t" + str(instrument.read_register(1637-1))
## Present Language Version (DLF format): X.Y.ZTT - UInt16
print "Present Language Version:\t" + str(instrument.read_register(1701-1))

#TODO Read Date/Time

##########################################
##Read Meter Setup and Status Registers ##
##########################################

# Number of Phases - UInt16
print "Number of Phases:\t" + str(instrument.read_register(2014-1))
# Number of Wires - UInt16
print "Number of Wires:\t" + str(instrument.read_register(2015-1))
#TODO: Power System Configuration - UInt16
print "Number of Wires:\t" + str(instrument.read_register(2016-1))
# Nominal Frequency - UInt16
print "Nominal Frequency\t" + str(instrument.read_register(2017-1)) + " Hz"
#TODO: Nominal Phase Order - UInt16
print "Nominal Phase Order\t" + str(instrument.read_register(2024-1)) 
# Number of VTs - UInt16
print "Number of VTs\t" + str(instrument.read_register(2025-1)) 
# VT Primary - Float32
print "VT Primary\t" + str(instrument.read_float(2026-1,3,2)) + " V"
# VT Secondary - UInt16
print "VT Secondary\t" + str(instrument.read_register(2028-1)) + " V"
# Number CTs - UInt16
print "Number CTs\t" + str(instrument.read_register(2029-1))
# CT Primary - UInt16
print "CT Primary\t" + str(instrument.read_register(2030-1)) + " A"
# CT Secondary - UInt16
print "CT Secondary\t" + str(instrument.read_register(2031-1)) + " A"
#TODO: VT Connection Type: - UInt16
print "VT Connection Type:\t" + str(instrument.read_register(2036-1))

#################################
## Command Interface Registers ##
#################################

#TODO

#############################
## Communication Registers ##
#############################

#TODO: Protocol - UInt16
print "Protocol:\t" + str(instrument.read_register(6500-1))
# Address - UInt16
print "Address:\t" + str(instrument.read_register(6501-1))
#TODO: Baud Rate - UInt16
print "Baud Rate:\t" + str(instrument.read_register(6502-1))
#TODO: Parity - UInt16
print "Parity:\t" + str(instrument.read_register(6503-1))

################################
## Basic Meter Data Registers ##
################################

#TODO if nan

# ====================================================#
# Current, voltage, power, power factor and frequency #
# ====================================================#

# - Current - #

# I1: phase 1 current - Float32
print "I1: phase 1 current\t" + str(instrument.read_float(3000-1,3,2)) + " A"
# I2: phase 2 current - Float32
print "I2: phase 2 current\t" + str(instrument.read_float(3002-1,3,2)) + " A"
# I3: phase 3 current - Float32
print "I3: phase 3 current\t" + str(instrument.read_float(3004-1,3,2)) + " A"
# In: Neutral current - Float32
print "Neutral current\t" + str(instrument.read_float(3006-1,3,2)) + " A"
# Current Avg - Float32
print "Current Avg\t" + str(instrument.read_float(3010-1,3,2)) + " A"


# - Voltage - #

# Voltage L1-L2 - Float32
print "Voltage L1-L2\t" + str(instrument.read_float(3020-1,3,2)) + " V"
# Voltage L2-L3 - Float32
print "Voltage L2-L3\t" + str(instrument.read_float(3022-1,3,2)) + " V"
# Voltage L3-L1 - Float32
print "Voltage L3-L1\t" + str(instrument.read_float(3024-1,3,2)) + " V"
# Voltage L-L Avg - Float32
print "Voltage L-L Avg\t" + str(instrument.read_float(3026-1,3,2)) + " V"
# Voltage L1-N - Float32
print "Voltage L1-N\t" + str(instrument.read_float(3028-1,3,2)) + " V"
# Voltage L2-N - Float32
print "Voltage L2-N\t" + str(instrument.read_float(3030-1,3,2)) + " V"
# Voltage L3-N - Float32
print "Voltage L3-N\t" + str(instrument.read_float(3032-1,3,2)) + " V"
# Voltage L-N Avg - Float32
print "Voltage L-N Avg\t" + str(instrument.read_float(3036-1,3,2)) + " V"


# - Power - #

#TODO better scaling W/kW etc ?

# Active Power Phase 1 - Float32
print "Active Power Phase 1\t" + str(instrument.read_float(3054-1,3,2)) + " kW"
# Active Power Phase 2 - Float32
print "Active Power Phase 2\t" + str(instrument.read_float(3056-1,3,2)) + " kW"
# Active Power Phase 3 - Float32
print "Active Power Phase 3\t" + str(instrument.read_float(3058-1,3,2)) + " kW"
# Total Active Power - Float32
print "Total Active Power\t" + str(instrument.read_float(3060-1,3,2)) + " kW"
# Reactive Power Phase 1 - Float32
print "Reactive Power Phase 1\t" + str(instrument.read_float(3062-1,3,2)) + " kVAR"
# Reactive Power Phase 2 - Float32
print "Reactive Power Phase 2\t" + str(instrument.read_float(3064-1,3,2)) + " kVAR"
# Reactive Power Phase 3 - Float32
print "Reactive Power Phase 3\t" + str(instrument.read_float(3066-1,3,2)) + " kVAR"
# Total Reactive Power - Float32
print "Total Reactive Power\t" + str(instrument.read_float(3068-1,3,2)) + " kVAR"
# Apparent Power Phase 1 - Float32
print "Apparent Power Phase 1\t" + str(instrument.read_float(3070-1,3,2)) + " kVA"
# Apparent Power Phase 2 - Float32
print "Apparent Power Phase 2\t" + str(instrument.read_float(3072-1,3,2)) + " kVA"
# Apparent Power Phase 3 - Float32
print "Apparent Power Phase 3\t" + str(instrument.read_float(3074-1,3,2)) + " kVA"
# Total Apparent Power - Float32
print "Total Apparent Power\t" + str(instrument.read_float(3076-1,3,2)) + " kVA"


# - Power Factor - #
#TODO Complex format ???

# Power Factor Phase 1 (Complex format) - Float32
print "Power Factor Phase 1\t" + str(instrument.read_float(3078-1,3,2))
# Power Factor Phase 2 (Complex format) - Float32
print "Power Factor Phase 2\t" + str(instrument.read_float(3080-1,3,2))
# Power Factor Phase 3 (Complex format) - Float32
print "Power Factor Phase 3\t" + str(instrument.read_float(3082-1,3,2))
#TODO Power Factor Total  - Float32
print "Power Factor Total\t" + str(instrument.read_float(3084-1,3,2))


# - Current Unbalance - #

#TODO if Nan

# Current Unbalance I1 - Float32
print "Current Unbalance I1\t" + str(instrument.read_float(3012-1,3,2)) + " %"
# Current Unbalance I2 - Float32
print "Current Unbalance I2\t" + str(instrument.read_float(3014-1,3,2)) + " %"
# Current Unbalance I3 - Float32
print "Current Unbalance I3\t" + str(instrument.read_float(3016-1,3,2)) + " %"
# Current Unbalance Worst - Float32
print "Current Unbalance Worst\t" + str(instrument.read_float(3018-1,3,2)) + " %"


# - Voltage Unbalance - #

#TODO if Nan

# Voltage Unbalance L1-L2 - Float32
print "Voltage Unbalance L1-L2\t" + str(instrument.read_float(3038-1,3,2)) + " %"
# Voltage Unbalance L2-L3 - Float32
print "Voltage Unbalance L2-L3\t" + str(instrument.read_float(3040-1,3,2)) + " %"
# Voltage Unbalance L3-L1 - Float32
print "Voltage Unbalance L3-L1\t" + str(instrument.read_float(3042-1,3,2)) + " %"
# Voltage Unbalance L-L Worst - Float32
print "Voltage Unbalance L-L Worst\t" + str(instrument.read_float(3044-1,3,2)) + " %"
# Voltage Unbalance L1-N - Float32
print "Voltage Unbalance L1-N\t" + str(instrument.read_float(3046-1,3,2)) + " %"
# Voltage Unbalance L2-N - Float32
print "Voltage Unbalance L2-N\t" + str(instrument.read_float(3048-1,3,2)) + " %"
# Voltage Unbalance L3-N - Float32
print "Voltage Unbalance L3-N\t" + str(instrument.read_float(3050-1,3,2)) + " %"
# Voltage Unbalance L-N Worst - Float32
print "Voltage Unbalance L-N Worst\t" + str(instrument.read_float(3052-1,3,2)) + " %"


# - Other Registers - #

# Tangent Phi (Reactive Factor) - Float32
print "Tangent Phi (Reactive Factor)\t" + str(instrument.read_float(3108-1,3,2))
# Frequency - Float32
print "Frequency\t" + str(instrument.read_float(3110-1,3,2)) + " Hz"
# Temperature - Float32
print "Temperature\t" + str(instrument.read_float(3132-1,3,2)) + " oC" 

# ============================================#
# Energy, energy by tariff and input metering #
# ============================================#
# Most energy values are available in both signed 64-bit integer and 32-bit floating point format

# --- Resets and active tariff information --- #

#TODO Energy Reset - Date/Time

#TODO Active Tariff - UInt16
# (Only modifiable in case of COM Control Mode Enabled):
# 0 = multi-tariff disabled
# 1-4 = rate 1 to rate 4
#print "Active Tariff\t" + str(instrument.read_register(4191-1))

#TODO Input Metering Accumulation Reset Date/Time

# --- Energy values - 64-bit integer --- #

# - Total Energy - #

# Total Active Energy Import - Int16
print "Total Active Energy Import\t" + str(instrument.read_register(3204-1,0,3,True)) + " Wh"
# Total Active Energy Export - Int16
print "Total Active Energy Export\t" + str(instrument.read_register(3208-1,0,3,True)) + " Wh"
# Total Reactive Energy Import - Int16
print "Total Reactive Energy Import\t" + str(instrument.read_register(3220-1,0,3,True)) + " VARh"
# Total Reactive Energy Export - Int16
print "Total Reactive Energy Export\t" + str(instrument.read_register(3224-1,0,3,True)) + " VARh"
# Total Apparent Energy Import - Int16
print "Total Apparent Energy Import\t" + str(instrument.read_register(3236-1,0,3,True)) + " VAh"
# Total Apparent Energy Export - Int16
print "Total Apparent Energy Export\t" + str(instrument.read_register(3240-1,0,3,True)) + " VAh"

# - Partial Energy Import - #

# Partial Active Energy Import - Int16
print "Partial Active Energy Import\t" + str(instrument.read_register(3256-1,0,3,True)) + " Wh"
# Partial Reactive Energy Import - Int16
print "Partial Reactive Energy Import\t" + str(instrument.read_register(3272-1,0,3,True)) + " VARh"
# Partial Apparent Energy Import - Int16
print "Partial Apparent Energy Import\t" + str(instrument.read_register(3288-1,0,3,True)) + " VAh"

# - Phase Energy Import - #

# Active Energy Import Phase 1 - Int16
print "Active Energy Import Phase 1\t" + str(instrument.read_register(3518-1,0,3,True)) + " Wh"
# Active Energy Import Phase 2 - Int16
print "Active Energy Import Phase 2\t" + str(instrument.read_register(3522-1,0,3,True)) + " Wh"
# Active Energy Import Phase 3 - Int16
print "Active Energy Import Phase 3\t" + str(instrument.read_register(3526-1,0,3,True)) + " Wh"
# Reactive Energy Import Phase 1 - Int16
print "Reactive Energy Import Phase 1\t" + str(instrument.read_register(3530-1,0,3,True)) + " VARh"
# Reactive Energy Import Phase 2 - Int16
print "Reactive Energy Import Phase 2\t" + str(instrument.read_register(3534-1,0,3,True)) + " VARh"
# Reactive Energy Import Phase 3 - Int16
print "Reactive Energy Import Phase 3\t" + str(instrument.read_register(3538-1,0,3,True)) + " VARh"
# Apparent Energy Import Phase 1 - Int16
print "Apparent Energy Import Phase 1\t" + str(instrument.read_register(3542-1,0,3,True)) + " VAh"
# Apparent Energy Import Phase 2 - Int16
print "Apparent Energy Import Phase 2\t" + str(instrument.read_register(3546-1,0,3,True)) + " VAh"
# Apparent Energy Import Phase 3 - Int16
print "Apparent Energy Import Phase 3\t" + str(instrument.read_register(3550-1,0,3,True)) + " VAh"

# - Energy by Tariff Import - #
# Rate 1 Active Energy Import - Int16
print "Rate 1 Active Energy Import\t" + str(instrument.read_register(4196-1,0,3,True)) + " Wh"
# Rate 2 Active Energy Import - Int16
print "Rate 2 Active Energy Import\t" + str(instrument.read_register(4200-1,0,3,True)) + " Wh"
# Rate 3 Active Energy Import - Int16
print "Rate 3 Active Energy Import\t" + str(instrument.read_register(4204-1,0,3,True)) + " Wh"
# Rate 4 Active Energy Import - Int16
print "Rate 4 Active Energy Import\t" + str(instrument.read_register(4208-1,0,3,True)) + " Wh"

# - Input Metering - #

# Input Metering Accumulation Channel 01 - Int16
print "Input Metering Accumulation Channel 01\t" + str(instrument.read_register(3558-1,0,3,True))
# Input Metering Accumulation Channel 02 - Int16
print "Input Metering Accumulation Channel 02\t" + str(instrument.read_register(3562-1,0,3,True))

# --- Energy values - 32-bit floating point --- # <-- Better

# - Total Energy - #

# Total Active Energy Import - Float32
print "Total Active Energy Import\t" + str(instrument.read_float(45166-1,3,2)) + " Wh"
# Total Active Energy Export - Float32
print "Total Active Energy Export\t" + str(instrument.read_float(45168-1,3,2)) + " Wh"
# Total Reactive Energy Import - Float32
print "Total Reactive Energy Import\t" + str(instrument.read_float(45170-1,3,2)) + " VARh"
# Total Reactive Energy Export - Float32
print "Total Reactive Energy Export\t" + str(instrument.read_float(45172-1,3,2)) + " VARh"
# Total Apparent Energy Import - Float32
print "Total Apparent Energy Import\t" + str(instrument.read_float(45174-1,3,2)) + " VAh"
# Total Apparent Energy Export - Float32
print "Total Apparent Energy Export\t" + str(instrument.read_float(45176-1,3,2)) + " VAh"

# - Partial Energy Import - #

# Partial Active Energy Import - Float32
print "Partial Active Energy Import\t" + str(instrument.read_float(45178-1,3,2)) + " Wh"
# Partial Reactive Energy Import - Float32
print "Partial Reactive Energy Import\t" + str(instrument.read_float(45180-1,3,2)) + " VARh"
# Partial Apparent Energy Import - Float32
print "Partial Apparent Energy Import\t" + str(instrument.read_float(45182-1,3,2)) + " VAh"

# - Phase Energy Import - #

# Active Energy Import Phase 1 - Float32
print "Active Energy Import Phase 1\t" + str(instrument.read_float(45184-1,3,2)) + " Wh"
# Active Energy Import Phase 2 - Float32
print "Active Energy Import Phase 2\t" + str(instrument.read_float(45186-1,3,2)) + " Wh"
# Active Energy Import Phase 3 - Float32
print "Active Energy Import Phase 3\t" + str(instrument.read_float(45188-1,3,2)) + " Wh"
# Reactive Energy Import Phase 1 - Float32
print "Reactive Energy Import Phase 1\t" + str(instrument.read_float(45190-1,3,2)) + " VARh"
# Reactive Energy Import Phase 2 - Float32
print "Reactive Energy Import Phase 2\t" + str(instrument.read_float(45192-1,3,2)) + " VARh"
# Reactive Energy Import Phase 3 - Float32
print "Reactive Energy Import Phase 3\t" + str(instrument.read_float(45194-1,3,2)) + " VARh"
# Apparent Energy Import Phase 1 - Float32
print "Apparent Energy Import Phase 1\t" + str(instrument.read_float(45196-1,3,2)) + " VAh"
# Apparent Energy Import Phase 2 - Float32
print "Apparent Energy Import Phase 2\t" + str(instrument.read_float(45198-1,3,2)) + " VAh"
# Apparent Energy Import Phase 3 - Float32
print "Apparent Energy Import Phase 3\t" + str(instrument.read_float(45200-1,3,2)) + " VAh"

# - Energy by Tariff Import - #
# Rate 1 Active Energy Import - Float32
print "Rate 1 Active Energy Import\t" + str(instrument.read_float(45206-1,3,2)) + " Wh"
# Rate 2 Active Energy Import - Float32
print "Rate 2 Active Energy Import\t" + str(instrument.read_float(45208-1,3,2)) + " Wh"
# Rate 3 Active Energy Import - Float32
print "Rate 3 Active Energy Import\t" + str(instrument.read_float(45210-1,3,2)) + " Wh"
# Rate 4 Active Energy Import - Float32
print "Rate 4 Active Energy Import\t" + str(instrument.read_float(45212-1,3,2)) + " Wh"

# - Input Metering - #

# Input Metering Accumulation Channel 01 - Float32
print "Input Metering Accumulation Channel 01\t" + str(instrument.read_float(45202-1,3,2))
# Input Metering Accumulation Channel 02 - Float32
print "Input Metering Accumulation Channel 02\t" + str(instrument.read_float(45204-1,3,2))

################################
## Demand ##
################################

#TODO

################################
## MinMax Reset ##
################################

#TODO

################################
## Minimum Values ##
################################

#TODO

################################
## Maximum Values ##
################################

#TODO

################################
## MinMax with Time Stamp ##
################################

#TODO

################################
## Power Quality ##
################################

#TODO

################################
## Alarms ##
################################

#TODO

################################
## Energy Log ##
################################

#TODO
