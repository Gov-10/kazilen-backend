from ninja import NinjaAPI, File, Router, UploadedFile
from django.shortcuts import get_object_or_404
from .models import ProfileImage
from .schemas import ImageResponse

router = Router()

@router.post("/upload", response=ImageResponse)
def upload_image(request, profileID: int, file: UploadedFile = File(...)):
    instance, created = ProfileImage.objects.update_or_create(
        profileID=profileID,
        defaults={'file': file}
    )
    
    return {
        "profileID": instance.profileID,
        "image_url": instance.file.url  
        }

@router.get("/get/{profileID}", response=ImageResponse)
def get_profile_image(request, profileID: int):
    image_entry = get_object_or_404(ProfileImage, profileID=profileID)
    return {
        "profileID": image_entry.profileID,
        "image_url": image_entry.file.url
    }
