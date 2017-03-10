#!/usr/bin/expect -f
spawn sftp -v -oIdentityFile=path username@XXX.XXX.XXX.XXX <<EOF
match_max 100000
# The following 3 lines are needed for the 1st time you run the script
expect "*?(yes/no)*"
send -- "yes"
send -- "\r"
expect "*?password:*"
send -- "... passwd..."
send -- "\r"
expect "sftp>" ; # put here string from your server prompt
set timeout 200
send "put /home/pi/backup/*.zip /home/VGWs_backup\r"
expect eof
