import smtplib
import netifaces as ni
import os
import datetime

print "----- IP Changed? ----"
print datetime.datetime.now()

ni.ifaddresses('tun0')
tun_ip = ni.ifaddresses('tun0')[2][0]['addr']
print 'cIP: ' + tun_ip

if (os.path.exists('/home/pi/ip.txt')):
    f = open('/home/pi/ip.txt', 'r')
    filedata = f.read()
    print 'oIP: ' + filedata
    f.close()
    if (str(filedata) == tun_ip):
        print "IP addresses match! No action Required!"
    else:
	print datetime.datetime.now()
        print "IPs don't match! Sending e-mail and Updating ip.txt"
        f = open('/home/pi/ip.txt', 'w')
        f.write(tun_ip)
        f.close()

	gmail_user = "eu.vimsen@gmail.com"
	gmail_pwd = "XXXXXX"
	FROM = 'eu.vimsen@gmail.com'
	TO = ['XXXXXX@api.pushover.net'] #must be a list
#TO = ['glimperop@cosmote.gr']
	SUBJECT = "genVGW1 (re)Connected ..."
	TEXT = 'http://'
	TEXT += tun_ip
	TEXT += ':8888/openhab.app?sitemap=glimperop'
#print TEXT

# Prepare actual message
	message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
	""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
	try:
#server = smtplib.SMTP(SERVER) 
    		server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
    		server.ehlo()
    		server.starttls()
    		server.login(gmail_user, gmail_pwd)
    		server.sendmail(FROM, TO, message)
 #server.quit()
    		server.close()
    		print 'successfully sent the mail (' + tun_ip +')'
	except:
    		print "failed to send mail"
