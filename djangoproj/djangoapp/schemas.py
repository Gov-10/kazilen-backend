from decimal import Decimal
from typing import List, Optional
from ninja import Field, ModelSchema, Schema
from .models import Customer, Worker, History
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic import field_validator
from datetime import datetime

class CustomerSchema(Schema):
    name:str
    address:str
    phoneNo:str
    email:str
    photo:Optional[str]=None
    @staticmethod
    def resolve_phoneNo(obj):
        return str(obj.phoneNo)

class WorkerSchema(ModelSchema):
    subcategory: List[str]
    phoneNo: PhoneNumber
    class Meta:
        model = Worker
        fields = "__all__"
    
    @staticmethod
    def resolve_phoneNo(obj):
        if not obj.phoneNo:
            return None
        return str(obj.phoneNo)
#class WorkerSchema(Schema):
#    name: str
#    address: str
#    phoneNo: str 
#    jobProfile: str
#    rating: float
#    price: Decimal
#    discription: str
class HistorySchema(Schema):
    id:int
    action: str
    timestmp: datetime
    customer_name: str
    @staticmethod
    def resolve_customer_name(obj):
        return obj.customer.name

class SendOTPSchema(Schema):
    phone : str

class VerifyOTPSchema(Schema):
    phone : str
    otp : str
