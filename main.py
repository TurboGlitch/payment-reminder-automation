import os
os.makedirs("output", exist_ok=True)

import schedule
import time

from sheets import get_pending_clients
from pdf_generator import generate_pdf
from emailer import ai_response
from emailer import send_email
from sheets import mark_as_reminded
from whatsapp import send_whatsapp

running = False

def process():
    global running
    if running:
        print("Previous run is still in progress, skipping...")
        return
    running = True
    try:
        clients, sheet = get_pending_clients()
        for client in clients:
            generate_pdf(client)
            bodywork = ai_response(client)
            if client["Contact Type"] == "Email":
                send_email(client, bodywork)
            else:
                send_whatsapp(client, bodywork)

            mark_as_reminded(sheet, client["row_number"])
    except Exception as e:
        print(f"Error! Couldn't get any data: {e}")
        return 
    finally:
        running = False
    
process()
schedule.every(24).hours.do(process)
while True:
    schedule.run_pending()
    time.sleep(1)