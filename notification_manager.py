import smtplib
import os

from twilio.rest import Client
from dotenv import load_dotenv  # pip install python-dotenv
load_dotenv("<LOCATION OF YOUR ENVIRONMENT VARIABLES FILE CONTAINING API AUTH TOKENS>")

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_GENERATED_NUM = os.getenv('TWILIO_GENERATED_NUM')
MY_NUM = '<YOUR PHONE NUMBER HERE>'
MY_EMAIL = '<YOUR_EMAIL@GMAIL.COM>'
#Google's 16-character-generated 'App passwords' must be used and 2-step verification must be enabled.
MY_EMAIL_PASSWORD = '<YOUR 16-CHARACTER APP PASSWORD>'
MAIL_PROVIDER_SMTP_ADDRESS = "smtp.gmail.com"


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    def send_text(self, message):

        message = self.client.messages.create(
            body=message,
            from_=TWILIO_GENERATED_NUM,
            to=MY_NUM
        )

    def send_emails(self, emails, email_message_body, google_flight_link):
        with smtplib.SMTP(MAIL_PROVIDER_SMTP_ADDRESS, 587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_EMAIL_PASSWORD)
            for email in emails:
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{email_message_body}\n{google_flight_link}".encode('utf-8'))

                print(f'Email sent to {email}')

