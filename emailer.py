import os
from dotenv import load_dotenv

import smtplib
from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText

from email.mime.base import MIMEBase
from email import encoders

from google import genai
from google.genai import types

from datetime import datetime 

from twilio.rest import Client

load_dotenv()

client_ai = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

account_sid = "HXb5b62575e6e4ff6129ad7c8efe1f983e"
auth_token = "13c4adb8d562da6503c3e07e9f5364e9"
whatsapp_client = Client(account_sid, auth_token)

def ai_response(client):

    now = datetime.now()
    date_only = now.date()

    req = f"""
        Write a short, professional payment reminder email, from company Turbo Studios.
        

        Client Name: {client['Client Name']}
        Business Name: {client['Business Name']} --> this is the client's business name
        Service: {client['Service/Item']}
        Amount Due: {client['Amount']}
        Due Date: {client['Due Date']}
        Status: {client['Status']}
        
        Keep it polite, brief, and mention the attached payment reminder PDF. Be a little harsh if the due date is gone.
        Sign off as my company, Turbo Tech.

        The date today is {date_only} so compare with the due date accordingly. No need to mention today's date though.
        """

    try:
        response = client_ai.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=req,
            config=types.GenerateContentConfig(
                system_instruction="""
                    you create a paragraph telling a client that their amount is due for their service or item by 
                    this date. professional business response. 
                    """
            )


        )

    except Exception as e:
        print(f"AI error: {e}")
        return f"This is a reminder that your payment of {client['Amount']} for {client['Service/Item']} is due on {client['Due Date']}. Please find the attached PDF for details."

    reply = response.text
    return reply    



def send_email(client, body):
    email = os.getenv("EMAIL")
    password = os.getenv("APP_PASSWORD")

    msg = MIMEMultipart()
    msg["Subject"] = f"Payment Reminder for {client["Client Name"]}"
    msg["From"] = email
    msg["To"] = client["Contact"]
    msg.attach(MIMEText(body, "plain"))


    attachment = MIMEBase("application", "octet-stream")
    attachment.set_payload(open(f"output/{client["Client Name"]} Reminder.pdf", "rb").read())
    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=f"{client["Client Name"]} Reminder.pdf")
    msg.attach(attachment)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email,password)
        server.sendmail(email, f"{client["Contact"]}", msg.as_string())
        print(f"Email Sent to {client["Client Name"]}")


