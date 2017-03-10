#!/bin/bash

	logfile="results.txt"
	eth0=1
	ppp0=0

#connect 3g
sudo bash /usr/bin/modem3g/sakis3g connect

#add route...
route add default gw 192.168.1.1 #to router pou to syndeoume

# connect VPN
echo "Connecting to VPN" && echo "Connecting to VPN" >> $logfile
sudo /home/pi/startVPN.sh #> /dev/null
sleep 15

ping -c 1 -I eth0 8.8.8.8 > /dev/null && status1=1 || status1=0
#echo status1, $status1

ping -c 1 -I ppp0 8.8.8.8 > /dev/null && status2=1 || status2=0
#echo status2, $status2

fallback=0

while true;do

	ping -c 1 -I eth0 8.8.8.8 > /dev/null
	check_one=$?

	ping -c 1 -I ppp0 8.8.8.8 > /dev/null
	check_two=$?


   #     ip=$(ifconfig | grep -oP "(?<=inet addr:).*?(?=Bcast)")      
     #  ip = $(ifconfig eth0 | grep 'inet addr:'| cut -d: -f2 | awk '{ print $1}')
   #     echo $ip
   #     if [[ $ip != " " ]]
   #     then
   #      echo "eth0 = " $ip
   #     else
   #      echo "eth0 IP = DOES NOT EXIST" 
   #     fi

	if [[ $check_one -eq 0 ]] 	#if eth0 is up
	then
		eth0=1
		echo "eth0 is up and routing exists" && echo "eth0 is up and routing exists" >> $logfile

		if [ $fallback -eq 1 ]
		then
			vtysh  -c "show run" –c "conf t" –c " no ip route 0.0.0.0/0 10.64.64.64 " –c "ip route 0.0.0.0/0 94.70.239.209" –c "end" –c "show run" > /dev/null 

			#kill VPN
			echo "Killing VPN" && echo "Killing VPN"  >> $logfile
		        service openvpn stop >/dev/null 2>&1
			kill $(pidof openvpn)
		        killall openvpn # just to be REALLY CERTAIN
			echo "routing via eth0" && echo "routing via eth0" >> $logfile
			fallback=0
        		sleep 5

			#Restart VPN
			echo "Restart VPN" && echo "Restart VPN"  >> $logfile
			sudo /home/pi/startVPN.sh #> /dev/null
			sleep 30
		fi
	else				#if eth0 is down
		eth0=0
		echo "eth0 is down" && echo "eth0 is down" >> $logfile
	fi

	if [[ $check_two -eq 0 ]]	#if ppp0 is up
	then
		ppp0=1
		echo "ppp0 is up and routing exists"  && echo "ppp0 is up and routing exists" >> $logfile
	else				#if ppp0 is down
		ppp0=0
		echo "ppp0 is down." && echo "ppp0 is down." >> $logfile
	fi
# GLL
	if [[ $eth0 -eq 1 ]] && [[ $ppp0 -eq 1 ]] #if eth0 is up AND ppp0 is up
	then
	echo "eth0 is UP and ppp0 is UP"
	fi

# GLL
	if [[ $eth0 -eq 1 ]] && [[ $ppp0 -eq 0 ]] #if eth0 is up AND ppp0 is down
	then
	echo "eth0 is UP and ppp0 is DOWN"
	fi

# GLL
	if [[ $eth0 -eq 0 ]] && [[ $ppp0 -eq 0 ]] #if eth0 is DOWN AND ppp0 is DOWN
	then
	echo "eth0 is DOWN and ppp0 is DOWN -> REBOOOOOOT"
	fi


	if [[ $eth0 -eq 0 ]] && [[ $ppp0 -eq 1 ]] #if eth0 is down AND ppp0 is up
	then
		if [ $fallback -eq 0 ]
		then
			echo "eth0 is down and routing via ppp0" && echo "eth0 is down and routing via ppp0" >> $logfile
			vtysh  -c "show run" –c "conf t" –c "no ip route 0.0.0.0/0 94.70.239.209" –c "ip route 0.0.0/0 10.64.64.64" –c "end" –c "show run" > /dev/null 
			fallback=1

			#kill VPN
			echo "Killing VPN" && echo "Killing VPN"  >> $logfile
		        service openvpn stop >/dev/null 2>&1
			kill $(pidof openvpn)
		        killall openvpn # just to be REALLY CERTAIN
        		sleep 2

			#Restart VPN
			echo "Restart VPN" && echo "Restart VPN"  >> $logfile
			sudo /home/pi/startVPN.sh #> /dev/null
			sleep 30
		else
			echo "not doing anything" && echo "not doing anything" >> $logfile
			echo $eth0
			echo $ppp0
		fi
	fi
	status1=eth0
	status2=ppp0
	sleep 10
done
