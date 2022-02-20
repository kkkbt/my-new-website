import os
import smtplib
from email.mime.text import MIMEText

MY_GMAIL = os.environ.get("MY_GMAIL")
WEBSITE_GMAIL= os.environ.get("WEBSITE_GMAIL")
WEBSITE_GMAIL_PW = os.environ.get("WEBSITE_GMAIL_PW")
jp='iso-2022-jp'

# def send_email(nickname, email_subject, email_content):
#
#     with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
#         connection.starttls()
#         connection.login(user=WEBSITE_GMAIL, password=WEBSITE_GMAIL_PW)
#         connection.sendmail(from_addr=WEBSITE_GMAIL,
#                             to_addrs=MY_GMAIL,
#                             msg=f"Subject:{nickname} {email_subject}\n\n{email_content}")


def send_email(nickname, email_subject, email_content):
    raw_message = f"{nickname}です。\n\nメッセージ\n{email_content}"
    msg = MIMEText(raw_message.encode(jp), 'plain', jp)
    msg["Subject"] = email_subject
    msg['From'] = WEBSITE_GMAIL
    msg['To'] = MY_GMAIL

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=WEBSITE_GMAIL, password=WEBSITE_GMAIL_PW)
        connection.send_message(msg)
