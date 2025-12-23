from django.db.models import Q, QuerySet
from typing_extensions import List
from typing import List, Optional
from ninja import FilterSchema, NinjaAPI, Query, Schema
from django.shortcuts import get_object_or_404
from .models import Customer, Worker, History
from .schemas import CustomerSchema, WorkerSchema, HistorySchema, SendOTPSchema, VerifyOTPSchema
import hashlib
from .utils.otp_generator import otp_gen
from redis import Redis
from dotenv import load_dotenv
load_dotenv()
api = NinjaAPI()

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


# @api.get("/worker/{name}", response=WorkerSchema)
# def getSingleWorker(request, name: str):
#     worker = get_object_or_404(Worker, name=name)
#     # return worker


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
   hashed = hashlib.sha256(otp.encode()).hexdigest()
   redis_client.setex(f"otp:{phone}", 600, hashed)
   print("OTP: ", otp)
   return {"otp" : otp}

@api.post("/verify-otp")
def verify_otp(request, payload: VerifyOTPSchema):
    key = f"otp:{payload.phone}"
    stored = redis_client.get(key)
    if not stored:
        return {"success": False, "error": "OTP expired or invalid"}
    input_hash = hashlib.sha256(data.otp.encode()).hexdigest()
    if input_hash != stored :
        return {"success": False, "error": "Invalid OTP entered"}
    redis_client.delete(key)
    return {"success": True}
