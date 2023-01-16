

from library.models import Signout
from django.conf import settings
import datetime
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

subject = 'SFU MSA Library - Outstanding Book [DO NOT REPLY]'
email_from = settings.EMAIL_HOST_USER
port = 465
password = settings.EMAIL_HOST_PASSWORD

def send_email_reminders():
    today = datetime.datetime.now()
    all_signouts = Signout.objects.filter(signed_back_in=False)
    # Create a secure SSL context
    context = ssl.create_default_context()

    for signout in all_signouts:
        # if outstanding books, send emails
        if (signout.signout_date + datetime.timedelta(days=21)).timestamp() <= today.timestamp():
            # has book for more than 3 weeks
            print("Sending Email")
            recipient = signout.user.email
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = email_from
            message["To"] = recipient
                    
            htmlMessage = f'''\
            <html>
            <body>
            <p> Salam {signout.user.first_name},</p>
            <p>
            This is a reminder that you have borrowed <strong>{signout.book.title}</strong> from the SFU MSA Library. If you have finished reading the book, we kindly ask that you return the book. If not, you can sign the book back out again.
            </p>
            <p>Jazakallah Khair,<br/> SFU MSA</p>
            </body>
            </html>
            '''
            # Turn these into plain/html MIMEText objects
            part = MIMEText(htmlMessage, "html")

            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            message.attach(part)

            with smtplib.SMTP_SSL("sfumsa.ca", port, context=context) as server:
                server.login(email_from, password)
                server.sendmail(email_from, recipient, message.as_string())
