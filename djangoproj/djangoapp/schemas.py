from decimal import Decimal
from typing import Any
from ninja import Field, ModelSchema, Schema
from pydantic import ConfigDict
from .models import Customer, Worker, History


class CustomerSchema(ModelSchema):
    class Meta:
        model = Customer
        fields = "__all__"


#class WorkerSchema(ModelSchema):
#    class Meta:
#        model = Worker
#        fields = "__all__"
class WorkerSchema(Schema):
    name: str
    address: str
    phoneNoObj: Any = Field(alias='phoneNo') 
    jobProfile: str
    rating: float
    price: Decimal
    discription: str
    @property
    def phoneNo(self) -> str:
        if self.phoneNoObj:
            return str(self.phoneNoObj)
        return ""
    class Config:
        json_encoders = {Decimal: str}
        from_attributes = True
        extra = "allow"

class HistorySchema(ModelSchema):
    class Meta:
        model = History
        fields = "__all__"
