from utils.otp_gen import otp_gene
import hashlib
from redis import Redis
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from schemas import CustomerSchema, WorkerSchema
load_dotenv()
app = FastAPI()

redis_client =Redis(
            host=os.getenv("REDIS_URL"),
            port =int(os.getenv("REDIS_PORT")), 
            password = os.getenv("REDIS_PASSWORD"),
            decode_responses=True
        )

#TODO: Common Auth lagado
@app.post("/start-pin")
def start_pin(payload: CustomerSchema):
    customer_phone=payload.customer_phone
    worker_phone=payload.worker_phone
    start_otp = otp_gene()
    hashed = hashlib.sha256(start_otp.encode()).hexdigest()
    redis_client.setex(f"start_otp:{customer_phone}:{worker_phone}", 86400, hashed)
    return {"startPin": start_otp}

@app.post("/confirm-start")
def confirmKaro(payload:WorkerSchema):
    #TODO: DB status updation and auth
    start_otp=payload.otp
    customer_phone=payload.customer_phone
    worker_phone=payload.worker_phone
    key=f"start_otp:{customer_phone}:{worker_phone}"
    otpRetr= redis_client.get(key)
    if otpRetr==start_otp:
        return {"message": "Pin matched successfully"}
    else:
        return {"message": "Pin did not match"}

@app.post("/confirm-end")
def confirmEnd(payload:WorkerSchema):
    #TODO:DB status updation and auth 
    customer_phone=payload.customer_phone
    worker_phone=payload.worker_phone
    end_otp=payload.otp
    key=f"end_otp:{customer_phone}:{worker_phone}"
    otpRetr=redis_client.get(key)
    if otpRetr==end_otp:
        return {"message": "Work completed successfully"}
    else:
        return {"message": "Pin did not match"}

#TODO: Common Auth lagado
@app.post("/end-pin")
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



