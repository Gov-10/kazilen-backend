from pydantic import BaseModel
class CustomerSchema(BaseModel):
    customer_phone:str
    worker_phone:str

class WorkerSchema(BaseModel):
    customer_phone:str
    worker_phone:str
    pin:str
