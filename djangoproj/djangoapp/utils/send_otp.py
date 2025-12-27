from dotenv import load_dotenv
import os
import requests
load_dotenv()
def send_otp_sms(phone: str, otp: str):
    url = ""
    payload = {
        "integrated_number": os.getenv("MSG91_WA_NUMBER"),
        "content_type": "template",
        "payload": {
            "to": phone,
            "type": "template",
            "template": {
                "name": "otp_template",
                "language": {"code": "en"},
                "components": [
                    {
                        "type": "body",
                        "parameters": [
                            {"type": "text", "text": otp}
                        ]
                    }
                ]
            }
        }
    }
    headers = {
        "authkey": os.getenv("MSG91_AUTH_KEY"),
        "Content-Type": "application/json",
    }

    r = requests.post(url, json=payload, headers=headers, timeout=5)
    r.raise_for_status()
