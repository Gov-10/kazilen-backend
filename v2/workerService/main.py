from fastapi import FastAPI, HTTPException, Request, Response, Depends, APIRouter
from sqlalchemy.orm import Session
import os, json, hashlib, jwt
from redis import Redis
from datetime import datetime, timedelta
from dotenv import load_dotenv
from database import sessionLocal, Workers
from utils.ot_gen import otp_gen
from utils.send_mess import send_sms
from utils.send_otp import sendOTP_SMS
from schema import SendOTPSchema, VerifyOTPSchema, CreateSchema, CheckSchema
load_dotenv()
import logging
app=FastAPI()
router=APIRouter(prefix="/workers")

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger=logging.getLogger("worker")
redis_client=Redis(host=os.getenv("REDIS_URL"), port=int(os.getenv("REDIS_PORT")), password=os.getenv("REDIS_PASSWORD"), decode_responses=True)
def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def chek():
    return {"status": "Running"}

@router.get("/send-otp")
def send_otp(payload: SendOTPSchema):
    phone=payload.phone
    otp= otp_gen()
    logger.info(json.dumps({"event": "otp_generated", "otp": otp}))
    hashed=hashlib.sha256(otp.encode()).hexdigest()
    redis_client.setex(f"otp:{phone}", 600, hashed)
    logger.info(json.dumps({"event": "otp_stored"}))
    sendOTP_SMS(otp=otp, recpient=phone)
    return {"status": True, "message": "OTP SENT SUCCESSFULLY"}

@router.post("/verify-otp")
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

@router.post("/check")
def db_check(response: Response, payload: CheckSchema, db: Session=Depends(get_db)):
    token=payload.token
    pay =jwt.decode(token, "supersecret", algorithms=["HS256"])
    phone=pay.get("sub")
    valid_phone = phone
    cus= db.query(Workers).filter(Workers.phone==valid_phone).first()
    if not cus:
        logger.error(json.dumps({"event": "user_not_found", "phone": valid_phone}))
        raise HTTPException(status_code=404, detail="User not found")
    payl={"iss": "kazilen-auth", "sub": phone, "exp": datetime.utcnow()+timedelta(days=7)}
    ref_token=jwt.encode(payl, "supersecret", algorithms=["HS256"])
    response.set_cookie(key="ref_token",value=ref_token, httponly=True, secure=True, samesite="lax", max_age=604800)
    logger.info(json.dumps({"event": "token_set", "message": "refresh token set in cookies"}))
    return {"message": "user found ji..."}

@router.post("/get-profile")
def get_profile(request: Request, db:Session=Depends(get_db)):
    token=request.cookies.get("ref_token")
    if not token:
        logger.error(json.dumps({"event": "token_not_found"}))
        raise HTTPException(status_code=401, detail="no tokens found")
    pay=jwt.decode(token, "supersecret", algorithms=["HS256"])
    phone=pay.get("sub")
    cus=db.query(Workers).filter(Workers.phone==phone).first()
    if not cus:
        logger.error(json.dumps({"event": "customer not found", "phone": phone}))
        raise HTTPException(status_code=404, detail="user not found")
    return {"gender": cus.gender, "name": cus.name, "address": cus.address, "phone": cus.phone, "dob": cus.dob, "rating": cus.rating, "categories": cus.categories, "sub_categories": cus.sub_categories}

@router.post("/logout")
def logou(request: Request, db:Session=Depends(get_db), response: Response):
    token=request.cookies.get("ref_token")
    if not token:
        logger.error(json.dumps({"event": "token_not_found"}))
        raise HTTPException(status_code=401, detail="no token found")
    response.delete_cookie("ref_token")
    return {"message": "logged out successfully"}

@router.post("/create-account")
def create_acc(payload: CreateSchema, db:Session=Depends(get_db)):
    gender, name=payload.gender, payload.name
    address, phone=payload.address, payload.phone
    dob, categories=payload.dob, payload.categories
    sub_categories=payload.sub_categories
    db_note=Workers(gender=gender, name=name, address=address, phone=phone, dob=dob, categories=categories, sub_categories=sub_categories)
    db.add(db_note)
    try:
        db.commit()
        logger.info(json.dumps({"event": "worker_created"}))
    except Exception as e:
        db.rollback()
        logger.error(json.dumps({"event": "db_error", "error": str(e)}))
        raise HTTPException(status_code=500, detail="database error")
    db.refresh(db_note)
    return {"message": f"worker created: {db_note.id}"}

@router.get("/list-workers")
def lis_workers(db:Session=Depends(get_db)):
    workers=db.query(Workers).all()
    res = []
    for worker in workers:
        det={"gender": worker.gender, "name": worker.name, "address": worker.address, "phone": worker.phone, "worker_id": worker.worker_id, "worker_status": worker.is_active, "rating": worker.rating, "description": worker.description, "categories": worker.categories, "sub_categories": worker.sub_categories}
        res.append(det)
    return {"workers": res}

@router.post("/get-history")
def get_his(request: Request, db:Session=Depends(get_db)):
    pass

@router.post("/details")
async def get_det(request: Request, db:Session=Depends(get_db)):
    try:
        body= await request.json()
        start_otp=body.get("start_otp")
        customer_phone=body.get("customer_phone")
        worker_phone=body.get("worker_phone")
        worker=db.query(Workers).filter(Workers.phone==worker_phone).first()
        if not worker:
            raise HTTPException(status_code=404, detail="worker does not exist")
        send_sms(customer_phone, worker_phone, start_otp)
        return {"worker_name": worker.name, "worker_status": worker.is_active, "worker_id": worker.worker_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="request failed")
        
app.include_router(router)





