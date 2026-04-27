from uuid import UUID
from django.db.models.functions import JSONArray
from djangoapp.models import Customer, History, Worker
from djangoapp.schemas import WorkerSchema
from django.db.models import Q, QuerySet
from typing_extensions import List
from typing import List, Optional
from ninja import FilterSchema, NinjaAPI, Query, Router, Schema
from django.shortcuts import get_object_or_404

import hashlib
from djangoapp.utils.otp_generator import otp_gen
from djangoapp.utils.send_otp import sendOTP_SMS, sendOTP_WHATSAPP
from redis import Redis
from dotenv import load_dotenv
import os
import logging
import secrets
from djangoapp.auth import CustomAuth
from django.db import connections
from django.db.utils import OperationalError

from djangoapp.schemas import (
    HistorySchema,
    SendOTPSchema,
    VerifyOTPSchema,
    WorkerSchema,
)

from .schemas import phonePayload, CreateWorkerSchema

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


@api.post("/checkproc", auth=CustomAuth())
def protected_check(request):
    phone = request.auth
    if not phone:
        return {"error": "User does not exist", "status": False}
    return {"message": f"Your phone number = {phone}"}


@api.post("/check", response={200: dict, 404: dict})
def unprotected_check(request, data: phonePayload):
    valid_phone = "+91" + data.phone
    exists = Worker.objects.filter(phoneNo=valid_phone).first()
    if exists:
        return 200, {"exists": True, "id": exists.id}
    else:
        return 404, {"messg": "yo no bud"}


class getPro(Schema):
    userID: UUID


@api.post("/get-profile", auth=CustomAuth(), response=WorkerSchema)
def get_profile(request, payload: getPro):
    data = get_object_or_404(Worker, id=payload.userID)
    return data


@api.get("/get-history", auth=CustomAuth(), response=List[HistorySchema])
def get_history(request):
    phone = request.auth
    if not phone:
        return {"error": "User does not exist", "status": False}
    customer = get_object_or_404(Customer, phoneNo=phone)
    details = History.objects.filter(customer=customer).order_by("-timestmp")
    return details


@api.post("/create-worker")
def create_worker(request, payload: CreateWorkerSchema):
    clean_phone = payload.phone.replace("+91", "").strip()
    worker = Worker.objects.create(
        name=payload.name,
        phoneNo=f"+91{clean_phone}",
        dob=payload.dob,
        gender=payload.gender,
        address=payload.address,
    )
    return {"message": f"Hello, {worker.name}", "status": True}


class giveSub(Schema):
    id: UUID

@api.post("/getSubCat", response=list)
def giveSubCat(request, payload: giveSub):
    clean_id = payload.id
    all_dat = get_object_or_404(Worker, id=clean_id)
    return all_dat.sub_categories


class UpdateSubSchema(Schema):
    worker_id: int
    subcategories: dict 

@api.post("/update-subcategories")
def update_worker_subcategories(request, data: UpdateSubSchema):
    worker = get_object_or_404(Worker, id=data.worker_id)
    
    worker.subcategories = data.subcategories
    worker.save()
    
    return {"success": True}


@api.get("/db_health")
def db_check(request):
    try:
        with db_conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            return {"status": "DB is up"}
    except OperationalError as e:
        print(f"DB ERROR: {e}")  # testing purposes only
        return {"status": "DB is down"}



class accept_booking(Schema):
    work : str


@api.post("/acceptBooking", auth= CustomAuth())
def acceptBooking(request, payload: accept_booking):
    work = get_object_or_404(History, id = payload.work)
    customerB = get_object_or_404(Customer, id = work.customer)
    workerB = get_object_or_404(Worker, id = work.worker)
    customerB.work_id = work.id
    workerB.work_id = work.id
    workerB.temp_id = None
    customerB.temp_id = None
    workerB.save()
    customerB.save()


class poll_this(Schema):
    id: str

@api.post('/pollThis', auth= CustomAuth())
def pollThis(request, payload: poll_this):
    workerA = get_object_or_404(Worker, id = payload.id)
    if workerA.temp_id is not None:
        return {"cmd": True}
    else:
        return {"cmd": False}




class unporc_profile(Schema):
    user_id: str


@api.post("/get_user_profile")
def unporc_get_profile(request, unporc_profile):
    user_id = request.user_id
    user = get_object_or_404(Customer, userID=user_id)
