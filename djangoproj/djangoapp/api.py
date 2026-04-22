from django.db.models import Q, QuerySet
from twilio.rest.ip_messaging.v2.service import channel
from typing_extensions import List
from typing import List, Optional
from ninja import FilterSchema, NinjaAPI, Query, Router, Schema
from django.shortcuts import get_object_or_404
from .models import Customer, Worker, History

from channels.layers import get_channel_layer

import asyncio

from .schemas import (
    CustomerSchema,
    WorkerSchema,
    HistorySchema,
    SendOTPSchema,
    VerifyOTPSchema,
    CreateAccountSchema,
    booking,
)

import hashlib
from .utils.otp_generator import otp_gen
from .utils.send_otp import sendOTP_SMS, sendOTP_WHATSAPP
from .utils.status_change import worker_update

from redis import Redis



from dotenv import load_dotenv
import os
import logging
import secrets
from .auth import CustomAuth
from django.db import connections
from django.db.utils import OperationalError

db_conn = connections["default"]  # will change once we migrate to neon

load_dotenv()

api = Router()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
redis_client = Redis(
    host=os.getenv("REDIS_URL"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
)

# class workerFilter(FilterSchema):
#     category: Optional[List[str]]
#     subcategory: Optional[List[str]]


@api.get("/worker", response=List[WorkerSchema])
def getAllWorker(request):
    return Worker.objects.all()


@api.get("/filterworker", response=List[WorkerSchema])
def getFilterWorker(request, category: str):
    filterk = {
            'sub_categories__contains' : [
                {'name': category, 'visible': True}
                ]
            }
    filterWorker = Worker.objects.filter(**filterk)
    return filterWorker

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
    if input_hash != stored:
        return {"success": False, "error": "Invalid OTP entered"}
    session_token = secrets.token_urlsafe(32)
    logger.info(f"SESSION_TOKEN: {session_token}")
    redis_client.setex(f"session:{session_token}", 86400, payload.phone)
    logger.info("SESSION TOKEN STORED IN REDIS")
    return {"success": True, "session": session_token}

@api.get("/check", auth=CustomAuth())
def protected_check(request):
    phone = request.auth
    if not phone:
        return {"error": "User does not exist", "status": False}
    return {"message": f"Your phone number = {phone}"}


class check_phoneNo(Schema):
    phone: str


@api.post("/check", response={200: CustomerSchema, 404: dict})
def unprotected_check(request, data: check_phoneNo):
    valid_phone = "+91" + data.phone
    exists = Customer.objects.filter(phoneNo=valid_phone).first()
    if exists:
        return 200, exists
    else:
        return 404, {"messg": "yo no bud"}


@api.get("/get-profile", auth=CustomAuth(), response=CustomerSchema)
def get_profile(request):
    phone = request.auth
    if not phone:
        return {"error": "User does not exist", "status": False}
    details = get_object_or_404(Customer, phoneNo=phone)
    return details


@api.get("/get-history", auth=CustomAuth(), response=List[HistorySchema])
def get_history(request):
    phone = request.auth
    if not phone:
        return {"error": "User does not exist", "status": False}
    customer = get_object_or_404(Customer, phoneNo=phone)
    details = History.objects.filter(customer=customer).order_by("-timestmp")
    return details


@api.post("/create-account")
def create_account(request, payload: CreateAccountSchema):
    customer = Customer.objects.create(**payload.dict())
    return {"message": "User created successfully", "name": customer.name}


@api.get("/db_health")
def db_check(request):
    try:
        with db_conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            return {"status": "DB is up"}
    except OperationalError as e:
        print(f"DB ERROR: {e}")  # testing purposes only
        return {"status": "DB is down"}


@api.post('/set-booking', auth = CustomAuth())
def setBooking(request, payload: booking):
    Booking = History.objects.create(customer=payload.customer, worker=payload.worker, action=payload.action)

