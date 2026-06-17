from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from database import sessionLocal, Bookings
import os, jwt, uuid, hashlib, requests
from redis import Redis 
from utils.otp_gen import gen_otp
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
redis_client=Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), password=os.getenv("REDIS_PASSWORD"), decode_responses=True)
app=FastAPI()
def get_db():
    db=sessionLocal()
    try:
        yield db 
    finally:
        db.close()

@app.get("/")
def chek():
    return {"status": "Running"}

@app.post("/book")
def book_worker(request: Request, payload: BookSchema, db:Session=Depends(get_db)):
    token=request.cookies.get("ref_token")
    if not token:
        raise HTTPException(status_code=404, detail="no token found")
    pay=jwt.decode(token, "supersecret", algorithms=["HS256"])
    if pay.get("iss") != "kazilen-auth":
        raise HTTPException(status_code=401, detail="invalid issuer")
    customer_phone=pay.get("sub")
    worker_phone=payload.worker_phone
    booking_id=str(uuid.uuid4())
    start_otp=gen_otp()
    try:
        resp=requests.post("http://worker-service/workers/details", json={"start_otp": start_otp, "customer_phone": customer_phone, "worker_phone": worker_phone}, timeout=5)
        resp.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail="failed to fetch")
    dt= resp.json()
    worker_name, worker_status=dt.get("worker_name"), dt.get("worker_status")
    if worker_status != True:
        raise HTTPException(status_code=403, detail="The specified worker is unreachable")
    worker_id=dt.get("worker_id")
    db_note=Bookings(booking_id=booking_id, customer=customer_phone, worker=worker_id, start_time=datetime.utcnow(), action=payload.action)
    db.add(db_note)
    try:
        db.commit()
    except Exeption as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="database error")
    db.refresh(db_note)
    hashed=hashlib.sha256(start_otp.encode()).hexdigest()
    redis_client.setex(f"{customer_phone}:{worker_phone}:otp", 7200, hashed)
    return {"booking_id": booking_id, "start_otp": start_otp, "worker_name": worker_name, "worker_id": worker_id}


@app.post("/start-work")
def start_book(request: Request, payload:StartSchema, db:Session=Depends(get_db)):
    start_otp, customer_phone=payload.start_otp, payload.customer_phone
    booking_id=payload.booking_id
    token=request.cookies.get("ref_token")
    if not token:
        raise HTTPException(status_code=404, detail="no token found")
    pay=jwt.decode(token, "supersecret", algorithms=["HS256"])
    worker_phone=pay.get("sub")
    key=f"{customer_phone}:{worker_phone}:otp"
    ot_hash=redis_client.get(key)
    sta_hash=hashlib.sha256(start_otp.encode()).hexdigest()
    if sta_hash != ot_hash:
        raise HTTPException(status_code=403, detail="otp does not match")
    book=db.query(Bookings).filter(Bookings.booking_id==booking_id).first()
    book.status="in-progress"
    db.add(book)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="database error")
    db.refresh(book)
    #TODO: Workers status update in db
    return {"message": "work has started"}






    


