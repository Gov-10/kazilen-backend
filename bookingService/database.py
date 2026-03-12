from pydantic_extra_types.phone_numbers import PhoneNumber
from datetime import datetime
from typing import List,Optional
class Worker(SQLModel, table=True):
    id: str= Field(default_factory=lambda:str(uuid.uuid4()), primary_key=True)
    name: str = Field()
    address: str = Field()
    phoneNo: PhoneNumber = Field(unique=True)
    is_Consult:bool= Field(default_factory=False)
    is_Hourly:bool=Field(default_factory=False)
    is_Fixed:bool=Field(default_factory=False)
    rating:float = Field(default_factory=0)
    dob:datetime=Field()
    gender:str=Field()
    location:str= Field()
    description:str=Field()
    history: List[History] = Relationship(back_populates="worker")

class Customer(SQLModel, table=True):
    name:str=Field()
    phoneNo:PhoneNumber=Field()
    email:str=Field(unique=True)
    gender:str=Field()
    dob:datetime=Field()
    history:List[History]=Relationship(back_populates="customer")
    


class History(SQLModel, table=True):
    id: str = Field(default_factory=lambda:str(uuid.uuid4()), primary_key=True)
    action:str= Field()
    timestmp:datetime=Field()
    worker:Optional["Worker"]=Relationship(back_populates="history")
    customer=Optional["Customer"]=Relationship(back_populates="customer")

