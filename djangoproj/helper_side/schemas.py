from ninja import ModelSchema, Schema
from djangoapp.models import Worker


class phonePayload(Schema):
    phone: str

class CreateWorkerSchema(Schema):
    phoneNo: str
    name: str
    dob: str
    gender:str
