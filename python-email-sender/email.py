import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64


def send_email(sender_email, sender_base64_password, to_address, subject, message):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_password = base64.b64decode(sender_base64_password).decode("utf-8")
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
