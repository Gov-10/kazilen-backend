from ninja import Router, Schema
from typing import List
from .models import Profile
import uuid

router = Router()

class imageOUT(Schema):
    url: str
    isPrimary: bool

class profileOUT(Schema):
    uniqueID: str
    name : str
    images : List[imageOUT]

@router.get("/profile/{uniqueID}", response=profileOUT)
def get_profile(request, uniqueID: uuid.UUID):
    profile = Profile.objects.get(uniqueID=uniqueID)
    return profile
