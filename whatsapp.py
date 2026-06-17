from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()


def send_whatsapp(client, message_body, pdf_path=None):

    account_sid = os.getenv("TWILIO_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    whatsapp_client = Client(account_sid, auth_token)

    whatsapp_client.messages.create(
        from_="whatsapp:+14155238886",
        body=message_body,
        to=f"whatsapp:+{client["Contact"]}"
    )
    print(f"Message sent to {client["Client Name"]}")

