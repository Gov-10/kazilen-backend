from typing import List
from ninja import ModelSchema, Schema
from .models import Customer, Worker, History


class CustomerSchema(ModelSchema):
    class Meta:
        model = Customer
        fields = "__all__"


class WorkerSchema(Schema):
    id: int
    name: str
    jobProfile: str
    address: str
    phoneNo: List(int)
    description: str


class HistorySchema(ModelSchema):
    class Meta:
        model = History
        fields = "__all__"
