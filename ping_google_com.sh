#!/bin/bash
PINGADDR="8.8.8.8"

function is_host_alive() # Returns success or failure as boolean
{
target="google.com"
count=$( ping -I tun0 -c 1 $target | grep icmp* | wc -l )
if [ $count -eq 0 ]
then
echo "Check 1 - NOK"
#echo -e "Rebooting .... | sudo reboot
else
echo "Check 1 - OK"
fi

#echo "Checking Connection to Internet ...."
	PACKETS=4
	TRIES=5
	IP=$1 # saving contents in $1 before is used
	echo "Check 2 - Pinging $IP"
	i=0
	while [ $i -lt $TRIES ]; do
		REQUEST=$(ping -I tun0 -qc $PACKETS $IP |grep packets| cut -d" " -f1,4)
		set -- $REQUEST
		echo -e "Try $i: $1 $2 \t"
		if [ $1 != $2 ]; then
#			echo "Bad news. $1 sent, $2 received."
			# exit
			exitcode=1
		else
#			echo "Great! $1 sent, $2 received."
			exitcode=0
		fi
		i=$(expr $i + 1)
	done
	return $exitcode
}

echo "----- New Round -------"
date

FOUNDtun=`grep "tun0:" /proc/net/dev`
if  [ -n "$FOUNDtun" ] ; then
echo "tun0 is up - no actions required!"
else
echo "tun0 is down"
echo -e "Restarting openVPN ... " | sudo sh /home/pi/restartVPN.sh
# shall re-establish the VPN tunnel and notify the new VPN_IP (10.8.0.xx)
fi

if is_host_alive $PINGADDR ; then
        echo "The VGW is connected to the Internet. Will check again in 10 mins!"
else
        echo -n "The gateway is not pingable :-( We should reboot ..."
        echo -e "Rebooting ...."  | sudo python /home/pi/sendReboot.py
#        echo -e "Rebooting ...."  | sudo reboot
fi
