import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import yaml

with open("secrets.yaml", "r") as file:
    secrets = yaml.safe_load(file)


def send_email(sender_email, sender_base64_password, to_address, subject, message):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_password = sender_base64_password
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_address
    msg["Subject"] = subject
    html_message = message
    msg.attach(MIMEText(html_message, "html"))
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_address, msg.as_string())
        print("Email sent successfully!")
        return True
    except Exception as e:
        print("Error sending email:", str(e))
        return False
    finally:
        server.quit()


send_email(
    secrets["sender_email"],
    secrets["sender_base64_password"],
    "phamousq@gmail.com",
    "test",
    "this is a test of python emailing",
)
