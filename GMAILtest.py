# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

msg = MIMEText("Hello World!")

me = 'source.email@gmail.com'
you = 'destination.email@gmail.com'

msg['Subject'] = 'HELLO!'
msg['From'] = me
msg['To'] = you

s = smtplib.SMTP_SSL('smtp.gmail.com:465')
s.login('source.email@gmail.com','your_password')
s.sendmail(me, [you], msg.as_string())
s.quit()

