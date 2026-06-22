from pydantic import BaseModel
class BookSchema(BaseModel):
    worker_name:str
    worker_phone:str
    worker_id:str
    action:str

class StartSchema(BaseModel):
    start_otp:str
    customer_phone:str
    booking_id:str

class EndSchema(BaseModel):
    worker_id: str
    booking_id:str

class EndVerifySchema(BaseModel):
    booking_id:str
    end_otp:str
    customer_phone:str

class FeedbackSchema(BaseModel):
    rating:int
    feedback:str
    booking_id:str
