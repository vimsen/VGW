import smtplib
import netifaces as ni

ni.ifaddresses('tun0')
ip = ni.ifaddresses('tun0')[2][0]['addr']
#print ip

gmail_user = "eu.vimsen@gmail.com"
gmail_pwd = "xxxxxxxx"
FROM = 'eu.vimsen@gmail.com'
TO = ['xxxxxx@api.pushover.net'] #must be a list
SUBJECT = "genVGW1 Started ..."
TEXT = 'http://'
TEXT += ip
TEXT += ':8888/openhab.app?sitemap=glimperop'
#print TEXT

# Prepare actual message
message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
try:
#server = smtplib.SMTP(SERVER) 
    server = smtplib.SMTP("smtp.gmail.com",587) #or port 465 doesn't seem to work!
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(FROM, TO, message)
#    server.quit()
    server.close()
    print 'successfully sent the mail'
except:
    print "failed to send mail"
