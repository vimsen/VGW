#!/bin/sh
# launcher.sh
sudo python /home/pi/PM3250/all_measurements.py

#!/bin/sh
LOGFILE=restart.txt

writelog() {
  now=`date`
  echo "$now $*" >> $LOGFILE
}

writelog "Starting"
while true ; do
  sudo python /home/pi/PM3250/all_measurements.py
  writelog "Exited with status $?"
  writelog "Restarting"
done
