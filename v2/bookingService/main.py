from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from database import sessionLocal, Bookings
import os, jwt, uuid, hashlib, requests, logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger=logging.getLogger("booking")
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
        logger.warning(json.dumps({"event":"token_not_found"}))
        raise HTTPException(status_code=404, detail="no token found")
    pay=jwt.decode(token, "supersecret", algorithms=["HS256"])
    if pay.get("iss") != "kazilen-auth":
        logger.warning(json.dumps({"event": "invalid_issuer", "issuer": pay.get("iss")}))
        raise HTTPException(status_code=401, detail="invalid issuer")
    customer_phone=pay.get("sub")
    worker_phone=payload.worker_phone
    booking_id=str(uuid.uuid4())
    start_otp=gen_otp()
    try:
        resp=requests.post("http://worker-service/workers/details", json={"start_otp": start_otp, "customer_phone": customer_phone, "worker_phone": worker_phone}, timeout=5)
        logger.info(json.dumps({"event": "worker_service_call", "status": resp.raise_for_status()}))
        resp.raise_for_status()
    except Exception as e:
        logger.error(json.dumps({"event": "worker_error", "error": str(e)}))
        raise HTTPException(status_code=500, detail="failed to fetch")
    dt= resp.json()
    worker_name, worker_status=dt.get("worker_name"), dt.get("worker_status")
    if worker_status != True:
        logger.warning(json.dumps({"event": "worker_inactive_during_booking", "status": worker_status}))
        raise HTTPException(status_code=403, detail="The specified worker is unreachable")
    worker_id=dt.get("worker_id")
    db_note=Bookings(booking_id=booking_id, customer=customer_phone, worker=worker_id, start_time=datetime.utcnow(), action=payload.action)
    db.add(db_note)
    try:
        db.commit()
        logger.info(json.dumps({"event": "booking_created", "id": db_note.id}))
    except Exeption as e:
        db.rollback()
        logger.error(json.dumps({"event": "db_error", "error": str(e)}))
        raise HTTPException(status_code=500, detail="database error")
    db.refresh(db_note)
    hashed=hashlib.sha256(start_otp.encode()).hexdigest()
    redis_client.setex(f"{customer_phone}:{worker_phone}:otp", 7200, hashed)
    logger.info(json.dumps({"event": "start_otp_set_in_redis"}))
    return {"booking_id": booking_id, "start_otp": start_otp, "worker_name": worker_name, "worker_id": worker_id}


@app.post("/start-work")
def start_book(request: Request, payload:StartSchema, db:Session=Depends(get_db)):
    start_otp, customer_phone=payload.start_otp, payload.customer_phone
    booking_id=payload.booking_id
    token=request.cookies.get("ref_token")
    if not token:
        logger.warning(json.dumps({"event": "token_not_found"}))
        raise HTTPException(status_code=404, detail="no token found")
    pay=jwt.decode(token, "supersecret", algorithms=["HS256"])
    worker_phone=pay.get("sub")
    key=f"{customer_phone}:{worker_phone}:otp"
    ot_hash=redis_client.get(key)
    sta_hash=hashlib.sha256(start_otp.encode()).hexdigest()
    if sta_hash != ot_hash:
        logger.warning(json.dumps({"event": "start_otp_mismatch"}))
        raise HTTPException(status_code=403, detail="otp does not match")
    book=db.query(Bookings).filter(Bookings.booking_id==booking_id).first()
    book.status="in-progress"
    db.add(book)
    try:
        db.commit()
        logger.info(json.dumps({"event": "booking_status_update", "status": book.status}))
    except Exception as e:
        db.rollback()
        logger.error(json.dumps({"event":"db_error", "error": str(e)}))
        raise HTTPException(status_code=500, detail="database error")
    db.refresh(book)
    #TODO: Workers status update in db
    return {"message": "work has started"}


@app.post("/end-work")
def end_wo(request: Request, db: Session=Depends(get_db), payload: EndSchema):
    token=request.cookies.get("ref_token")
    if not token:
        logger.info(json.dumps({"event": "token_not_found"}))
        raise HTTPException(status_code=404, detail="no token found")
    pay=jwt.decode(token, "supersecret", algorithms=["HS256"])
    customer_phone=pay.get("sub")
    worker_phone=payload.worker_phone
    try:
        resp = requests.post("http://worker-service/workers/details", json={"customer_phone": customer_phone, "worker_phone": worker_phone}, timeout=5)
        logger.info(json.dumps({"event": "worker_service_call", "status": resp.raise_for_status()}))
        resp.raise_for_status()
    except Exception as e:
        logger.error(json.dumps({"event": "worker_error", "error": str(e)}))
        raise HTTPException(status_code=500, detail="error fetching worker id")
    resp=resp.json()
    worker_id, worker_status=resp.get("worker_id"), resp.get("worker_status")
    if worker_status != True:
        logger.warning(json.dumps({"event": "worker_inactive_during_booking"}))
        raise HTTPException(status_code=403, detail="Worker not active")
    booking_id=payload.get("booking_id")
    if not booking_id:
        logger.warning(json.dumps({"event": "booking_id_not_found"}))
        raise HTTPException(status_code=404,detail="booking id not provided" )
    book=db.query(Bookings).filter(Bookings.booking_id==booking_id, Bookings.worker==worker_id, Bookings.customer==customer_phone).first()
    if not book:
        logger.warning(json.dumps({"event": "booking_not_found", "id": booking_id}))
        raise HTTPException(status_code=404, detail="no booking found")
    book.status = "end-verification-pending"
    db.add(book)
    try:
        db.commit()
        logger.info(json.dumps({"event": "booking_status_update", "status": book.status}))
    except Exception as e:
        db.rollback()
        logger.error(json.dumps({"event": "db_error", "error": str(e)}))
        raise HTTPException(status_code=500, detail="database error")
    db.refresh(book)
    end_otp = otp_gen()
    key=f"{customer_phone}:{worker_phone}:end_otp"
    hashed=hashlib.sha256(end_otp.encode()).hexdigest()
    redis_client.setex(key, 7200, hashed)
    logger.info(json.dumps({"event": "end_otp_set_redis"}))
    return {"end_otp": end_otp, "booking_id": booking_id}

@app.post("/verify-end")
def verify_en(db: Session=Depends(get_db), request: Request, payload: EndVerifySchema):
    token = request.cookies.get("ref_token")
    if not token:
        logger.info(json.dumps({"event": "token_not_found"}))
        raise HTTPException(status_code=404, detail="no token found")
    booking_id, end_otp=payload.booking_id, payload.end_otp
    customer_phone=payload.customer_phone
    pay=jwt.decode(token, "supersecret", algorithms=["HS256"])
    worker_phone=pay.get("sub")
    key=f"{customer_phone}:{worker_phone}:end_otp"
    hashed=hashlib.sha256(end_otp.encode()).hexdigest()
    ot=redis_client.get(key)
    if hashed != ot:
        logger.warning(json.dumps({"event": "end_otp_mismatch"}))
        raise HTTPException(status_code=401, detail="otp does not match")
    book= db.query(Bookings).filter(Bookings.booking_id==booking_id, Bookings.customer==customer_phone)
    book.status="completed"
    book.end_time=datetime.utcnow()
    db.add(book)
    try:
        db.commit()
        logger.info(json.dumps({"event": "booking_status_update", "status": book.status, "end_time": book.end_time}))
    except Exception as e:
        db.rollback()
        logger.error(json.dumps({"event": "db_error", "error": str(e)}))
        raise HTTPException(status_code=500, detail="database error")
    db.refresh(book)
    #TODO: worker db state updation
    return {"message": "Customer says thank you for your service"}

@app.post("/feedback")
def feedb(request: Request, payload: FeedbackSchema, db:Session=Depends(get_db)):
    token=request.cookies.get("ref_token")
    if not token:
        logger.warning(json.dumps({"event": "token_not_found"}))
        raise HTTPException(status_code=404, detail="no token found")
    rating, feedback=payload.rating, payload.feedback
    booking_id=payload.booking_id
    pay=jwt.decode(token, "supersecret", algorithms=["HS256"])
    customer_phone=pay.get("sub")
    book=db.query(Bookings).filter(Bookings.booking_id==booking_id, Bookings.customer==customer_phone).first()
    if not book:
        logger.warning(json.dumps({"event": "booking_not_found", "booking_id": booking_id}))
        raise HTTPException(status_code=404, detail="booking not found")
    book.rating=rating
    book.feeback=feedback
    db.add(book)
    try:
        db.commit()
        logger.info(json.dumps({"event": "booking_feedback_added"}))
    except Excepion as e:
        db.rollback()
        logger.error(json.dumps({"event": "db_error", "error": str(e)}))
        raise HTTPException(status_code=500, detail="database error")
    db.refresh(book)
    return {"message": "thank you for your valuable feedback"}





    





    



    


