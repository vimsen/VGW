#!/bin/bash

ip=$(ifconfig | grep -oP "(?<=inet addr:).*?(?=Bcast)")      
#  ip = $(ifconfig eth0 | grep 'inet addr:'| cut -d: -f2 | awk '{ print $1}')
        echo $ip
	if [[ $ip != " " ]]
        then
         echo "eth0 = " $ip
        else
         echo "eth0 IP = DOES NOT EXIST" 
        fi
