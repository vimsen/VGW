#!/usr/bin/expect -f
spawn openvpn --client --config /etc/openvpn/VP33.conf
match_max 100000
expect "*?Password:*"
send -- "XXXXXX"
send -- "\r"
expect eof

