#!/bin/sh
# The following packages should have been installed ...
sudo apt-get install -y expect zip ftp
echo "Removing previous files"
sudo rm -r /home/pi/backup/*
#sudo rm /home/pi/backup/*.*
echo "Creating Folders"
sudo mkdir /home/pi/backup
sudo mkdir /home/pi/backup/openhab
sudo mkdir /home/pi/backup/openhab/configurations
sudo mkdir /home/pi/backup/openhab/addons
sudo mkdir /home/pi/backup/cron
echo "Copying Files ..."
sudo cp -r /opt/openhab/configurations/* /home/pi/backup/openhab/configurations
sudo cp -r /opt/openhab/addons/* /home/pi/backup/openhab/addons
sudo cp -r /home/pi/cron/* /home/pi/backup/cron
sudo cp /opt/openhab/start.sh /home/pi/backup/openhab/start.sh
sudo cp /home/pi/*.sh /home/pi/backup/
sudo cp /home/pi/*.py /home/pi/backup/
sudo cp /home/pi/*.txt /home/pi/backup/
sleep 2
echo "Compressing Files ..."
#Enter the name of the VGW
sudo zip -r /home/pi/backup/xxxVGW-`date +%d%m%y`.zip /home/pi/backup/
sleep 2
echo "Uploading Files to RDM/EDMS ..."
sudo expect /home/pi/upload.sh
echo "Completed!"

