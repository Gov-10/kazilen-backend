from ninja import Schema, NinjaAPI
from typing import List
from .models import Profile
import uuid

api = NinjaAPI()

class imageOUT(Schema):
    url: str
    isPrimary: bool

class profileOUT(Schema):
    uniqueID: str
    name : str
    images : List[imageOUT]

@api.get("/profile/{uniqueID}", response=profileOUT)
def get_profile(request, uniqueID: uuid.UUID):
    profile = Profile.objects.get(uniqueID=uniqueID)
    return profile

@api.get("/ola", response= str)
def ola(request):
    return "ola"
