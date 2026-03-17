from utils.otp_gen import otp_gene
import hashlib
from redis import Redis
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
load_dotenv()
app = FastAPI()

redis_client =Redis(
            host=os.getenv("REDIS_URL"),
            port =int(os.getenv("REDIS_PORT")), 
            password = os.getenv("REDIS_PASSWORD"),
            decode_responses=True
        )

#TODO: Common Auth lagado
@app.get("/start-pin")
def start_pin(payload: CustomerSchema):
    customer_phone=payload.customer_phone
    worker_phone=payload.worker_phone
    start_otp = otp_gene()
    hashed = hashlib.sha256(start_otp.encode()).hexdigest()
    redis_client.setex(f"start_otp:{customer_phone}:{worker_phone}", 86400, hashed)
    #TODO: Change the is_Live status of worker
    return {"startPin": start_otp}

#TODO: Common Auth lagado
@app.get("/end-pin")
def end_pin(payload: CustomerSchema):
    customer_phone=payload.customer_name
    worker_phone=payload.worker_phone
    end_otp=otp_gene()
    key=f"start_otp:{customer_phone}:{worker_phone}"
    stored = redis_client.get(key)
    if key is not None:
        hashed=hashlib.sha256(end_otp.encode()).hexdigest()
        redis_client.setex(f"end_otp:{customer_phone}:{worker_phone}", 86400, hashed)
        return {"endPin": end_otp}
    else:
        raise HTTPException(status_code=404, detail="No such job exists")

    




