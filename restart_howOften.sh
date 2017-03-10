#!/bin/sh
ps auxw | grep howOften_LRpowerREST | grep -v grep > /dev/null
if [ $? != 0 ] 
then
echo "NOT running"
python /home/pi/howOften_LRpowerREST.py >> /dev/null &
else
echo "HowOften = running"
fi

