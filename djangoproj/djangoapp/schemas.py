from decimal import Decimal
from typing import List
from ninja import Field, ModelSchema, Schema
from .models import Customer, Worker, History
from pydantic_extra_types.phone_numbers import PhoneNumber

class CustomerSchema(ModelSchema):
    class Meta:
        model = Customer
        fields = "__all__"


class WorkerSchema(ModelSchema):
    subcategory: List[str]
    phoneNo: PhoneNumber
    class Meta:
        model = Worker
        fields = "__all__"

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
