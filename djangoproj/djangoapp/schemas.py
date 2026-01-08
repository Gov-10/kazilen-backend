from decimal import Decimal
from typing import List, Optional
from ninja import Field, ModelSchema, Schema
from .models import Customer, Worker, History
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic import field_validator

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
class HistorySchema(ModelSchema):
    class Meta:
        model = History
        fields = "__all__"

class SendOTPSchema(Schema):
    phone : str

class VerifyOTPSchema(Schema):
    phone : str
    otp : str
