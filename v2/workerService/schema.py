from pydantic import BaseModel
from datetime import datetime
from typing import List
class SendOTPSchema(BaseModel):
    phone:str

class VerifyOTPSchema(BaseModel):
    phone:str
    otp:str

class CheckSchema(BaseModel):
    token:str

class CreateSchema(BaseModel):
    gender:str
    name:str
    address:str
    phone:str
    dob:datetime
    categories:str
    sub_categories:List[str]
