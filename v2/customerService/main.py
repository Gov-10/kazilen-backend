from fastapi import FastAPI, HTTPException, Depends, Response, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import os, json, hashlib, jwt
from redis import Redis
from datetime import datetime, timedelta
from schema import SendOTPSchema, VerifyOTPSchema, CheckSchema, CreateSchema
from dotenv import load_dotenv
from database import sessionLocal, Customers
load_dotenv()
import logging

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()

app=FastAPI()
logging.basiConfig(level=logging.INFO, format="%(message)s")
logger=logging.getLogger("auth")
redis_client = Redis(
    host=os.getenv("REDIS_URL"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
)

@app.get("/")
def chek():
    return {"status": "Running"}

@app.post("/send-otp")
def send_otp(payload: SendOTPSchema):
    phone=payload.phone
    otp= otp_gen()
    logger.info(json.dumps({"event": "otp_generated", "otp": otp}))
    hashed=hashlib.sha256(otp.encode()).hexdigest()
    redis_client.setex(f"otp:{phone}", 600, hashed)
    logger.info(json.dumps({"event": "otp_stored"}))
    sendOTP_SMS(otp=otp, recpient=phone)
    return {"status": True, "message": "OTP SENT SUCCESSFULLY"}

@app.post("/verify-otp")
def verify_otp(payload: VerifyOTPSchema):
    key= f"otp:{payload.phone}"
    stored=redis_client.get(key)
    if not stored:
        logger.error(json.dumps({"event": "otp_missing"}))
        raise HTTPException(status_code=404, detail="otp not found")
    ot=payload.otp
    input_hash=hashlib.sha256(ot.encode()).hexdigest()
    if input_hash != stored:
        logger.error(json.dumps({"event": "invalid_otp", "otp": ot}))
        raise HTTPException(status_code=401, detail="wrong OTP entered")
    pay= {"iss": "kazilen-auth", "sub":payload.phone, "exp": datetime.utcnow()+timedelta(seconds=600)}
    token= jwt.encode(pay, "supersecret", algorithms=["HS256"])
    redis_client.delete(key)
    return {"token": token}

@app.post("/check")
def db_check(response: Response, payload: CheckSchema, db: Session=Depends(get_db)):
    token=payload.token
    pay =jwt.decode(token, "supersecret", algorithms=["HS256"])
    phone=pay.get("sub")
    valid_phone = "+91"+phone
    cus= db.query(Customers).filter(Customers.phone==valid_phone).first()
    if not cus:
        logger.error(json.dumps({"event": "user_not_found", "phone": valid_phone}))
        raise HTTPException(status_code=404, detail="User not found")
    payl={"iss": "kazilen-auth", "sub": phone, "exp": datetime.utcnow()+timedelta(days=7)}
    ref_token=jwt.encode(payl, "supersecret", algorithms=["HS256"])
    response.set_cookie(key="ref_token",value=ref_token, httponly=True, secure=True, samesite="lax", max_age=604800)
    logger.info(json.dumps({"event": "token_set", "message": "refresh token set in cookies"}))
    return {"message": "user found ji..."}

@app.post("/get-profile")
def get_profile(request: Request, db:Session=Depends(get_db)):
    token=request.cookies.get("ref_token")
    if not token:
        logger.error(json.dumps({"event": "token_not_found"}))
        raise HTTPException(status_code=401, detail="no tokens found")
    pay=jwt.decode(token, "supersecret", algorithms=["HS256"])
    phone=pay.get("sub")
    cus=db.query(Customers).filter(Customers.phone==phone).first()
    if not cus:
        logger.error(json.dumps({"event": "customer not found", "phone": phone}))
        raise HTTPException(status_code=404, detail="user not found")
    return {"gender": cus.gender, "name": cus.name, "phone": cus.phone, "dob": cus.dob, "address": cus.address}

@app.post("/logout")
def logou(request: Request, db:Session=Depends(get_db), response: Response):
    token=request.cookies.get("ref_token")
    if not token:
        logger.error(json.dumps({"event": "token_not_found"}))
        raise HTTPException(status_code=401, detail="no token found")
    response.delete_cookie("ref_token")
    return {"message": "logged out successfully"}

@app.post("/create-account")
def create_acc(payload: CreateSchema, db:Session=Depends(get_db)):
    name, phone=payload.name, payload.phone
    address=payload.address
    gender, dob=payload.gender, payload.dob
    db_note=Customers(name=name, phone=phone, gender=gender, dob=dob, address=address)
    db.add(db_note)
    try:
        db.commit()
        logger.info(json.dumps({"event": "account_created", "id": db_note.id}))
    except Exception as e:
        db.rollback()
        logger.error(json.dumps({"event": "db_error", "error": str(e)}))
        raise HTTPException(status_code=500, detail="database error")
    db.refresh(db_note)
    return JSONResponse(status_code=200, content={"message": "user created success"})

@app.post("/get-history")
def get_his(request: Request, db:Session=Depends(get_db)):
    pass

    



    
    
    
    

    
    
