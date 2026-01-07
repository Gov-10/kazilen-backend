from django.db.models import Q, QuerySet
from typing_extensions import List
from typing import List, Optional
from ninja import FilterSchema, NinjaAPI, Query, Schema
from django.shortcuts import get_object_or_404
from .models import Customer, Worker, History
from .schemas import CustomerSchema, WorkerSchema, HistorySchema, SendOTPSchema, VerifyOTPSchema
import hashlib
from .utils.otp_generator import otp_gen
from .utils.send_otp import sendOTP_SMS, sendOTP_WHATSAPP
from redis import Redis
from dotenv import load_dotenv
import os
import logging
import secrets
from .auth import CustomAuth
#Log statements that expose vital info shall be removed later. This project is currently not in production
load_dotenv()
api = NinjaAPI()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
redis_client = Redis(
        host = os.getenv("REDIS_URL"), 
        port = int(os.getenv("REDIS_PORT")),
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True
        )

# class workerFilter(FilterSchema):
#     category: Optional[List[str]]
#     subcategory: Optional[List[str]]

@api.get("/worker", response=List[WorkerSchema])
def getAllWorker(request):
    return Worker.objects.all()


@api.get("/filterworker", response=List[WorkerSchema])
def getFilterWorker(
    request,
    category: Optional[str] = Query(None),
    subcategory: Optional[str] = Query(None),
):
    filters = Q()
    if category:
        filters &= Q(category=category)
    if subcategory:
        filters &= Q(subcategory=subcategory)
    workers = Worker.objects.filter(filters)
    return workers

@api.post("/send-otp")
def send_otp(request, payload: SendOTPSchema):
   phone = payload.phone
   otp = otp_gen()
   logger.info(f"OTP: {otp}")
   hashed = hashlib.sha256(otp.encode()).hexdigest()
   logger.info(f"Hashed: {hashed}")
   redis_client.setex(f"otp:{phone}", 600, hashed)
   logger.info("STORED IN REDIS")
   sendOTP_SMS(otp=otp, recpient=phone)
   return {"status": True, "message": "OTP Sent successfully"}

@api.post("/verify-otp")
def verify_otp(request, payload: VerifyOTPSchema):
    key = f"otp:{payload.phone}"
    stored = redis_client.get(key)
    if not stored:
        return {"success": False, "error": "OTP expired or invalid"}
    input_hash = hashlib.sha256(payload.otp.encode()).hexdigest()
    if input_hash != stored :
        return {"success": False, "error": "Invalid OTP entered"}
    session_token = secrets.token_urlsafe(32)
    logger.info(f"SESSION_TOKEN: {session_token}")
    redis_client.setex(f"session:{session_token}", 86400, payload.phone)
    logger.info("SESSION TOKEN STORED IN REDIS")
    return {"success": True, "session": session_token}

@api.get("/check", auth=CustomAuth())
def protected_check(request):
    phone = request.auth
    return {"message" : f"Your phone number = {phone}"}

