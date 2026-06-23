import os
from dotenv import load_dotenv
from twilio.rest import Client
load_dotenv()
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
COMPANY_NUMBER = os.getenv("COMPANY_NUMBER")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_sms(customer_phone, worker_phone, start_otp):
    try:
        client.messages.create(body=f"You have been assigned task, customer phone: {customer_phone}", from_=COMPANY_NUMBER, to=f'+{worker_phone}')
    except:
        print("error ji")


