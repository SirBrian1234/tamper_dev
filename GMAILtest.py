# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

source = 'source.email@gmail.com'
password = 'your_password'

destination = 'destination.email@anything.com'

msg = MIMEText("Hello World!")
msg['Subject'] = 'HELLO! This is a test email.'
msg['From'] = source
msg['To'] = destination

s = smtplib.SMTP_SSL('smtp.gmail.com:465')
s.login(source,password)
s.sendmail(source, [destination], msg.as_string())
s.quit()
