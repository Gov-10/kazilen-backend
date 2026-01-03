import os
from dotenv import load_dotenv
from twilio.rest import Client
load_dotenv()

ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
COMPANY_NUMBER = os.getenv("COMPANY_NUMBER")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def sendOTP_SMS(recpient, otp):
    try:
        client.messages.create(
            body=f'your otp is {otp}',
            from_=COMPANY_NUMBER,
            to=f'+{recpient}'
            )
    except:
        print("error ho gaya ji")


def sendOTP_WHATSAPP(recpient, otp):
    try:
        client.messages.create(
            body=f'your otp is {otp}',
            from_=f'whatsapp:{COMPANY_NUMBER}',
            to=f'whatsapp:+{recpient}'
            )
    except:
        print("error ho gaya ji")
