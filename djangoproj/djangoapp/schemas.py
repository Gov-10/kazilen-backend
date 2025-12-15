from typing import List, Literal
from ninja import ModelSchema, Schema
from pydantic import ConfigDict
from .models import Customer, Worker, History

jobIdentifier = Literal[
    "vehicle", "health", "carpenter", "electrician", "home", "appliance", "labour"
]


class CustomerSchema(ModelSchema):
    class Meta:
        model = Customer
        fields = "__all__"


class WorkerSchema(Schema):
    id: int
    name: str
    jobProfile: str
    address: str
    phoneNo: List[int]
    description: str


class HistorySchema(ModelSchema):
    class Meta:
        model = History
        fields = "__all__"
