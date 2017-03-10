import smtplib
import netifaces as ni

ni.ifaddresses('ppp0')
ip = ni.ifaddresses('ppp0')[2][0]['addr']
#print ip

gmail_user = "eu.vimsen@gmail.com"
gmail_pwd = "XXXXX"
FROM = 'eu.vimsen@gmail.com'TO = ['XXXXXX@api.pushover.net'] #must be a list
SUBJECT = "VGW Lost Connection to the Internet. Rebooting ..."
TEXT = "(4G) IP Address ... "
TEXT += ip
print TEXT

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
    print 'successfully sent the mail'
except:
    print "failed to send mail"
