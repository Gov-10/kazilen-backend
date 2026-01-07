from ninja.security import HttpBearer
from redis import Redis
from dotenv import load_dotenv
import os
load_dotenv()
redis_client = Redis(
    host = os.getenv("REDIS_URL"),
    port = int(os.getenv("REDIS_PORT")),
    password = os.getenv("REDIS_PASSWORD"),
    decode_responses = True
        )

class CustomAuth(HttpBearer):
    def authenticate(self, request, token):
        key = f"session:{token}"
        phone = redis_client.get(key)
        if not phone:
            return None
        return phone
