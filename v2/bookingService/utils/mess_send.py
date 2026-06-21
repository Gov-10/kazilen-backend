import os
from dotenv import load_dotenv
load_dotenv()
from twilio.rest import Client
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
COMPANY_NUMBER = os.getenv("COMPANY_NUMBER")



def send_sms(customer_phone, worker_phone):
     try:
        client.messages.create(body=f"You have been assigned task, customer phone: {customer_phone}", from_=COMPANY_NUMBER, to=f'+{worker_phone}')
    except:
        print("error ji")
