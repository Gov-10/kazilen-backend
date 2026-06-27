from pydantic import BaseModel
from datetime import date
class SendOTPSchema(BaseModel):
    phone:str

class VerifyOTPSchema(BaseModel):
    phone: str
    otp: str

class CheckSchema(BaseModel):
    token: str

class CreateSchema(BaseModel):
    name:str
    phone:str
    address:str
    gender: str
    dob:date

