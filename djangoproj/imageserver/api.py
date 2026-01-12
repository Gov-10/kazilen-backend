from uuid import UUID
from typing import List
from ninja import NinjaAPI, File, Router, UploadedFile
from django.shortcuts import get_object_or_404
from .models import ProfileImage
from .schemas import ImageResponse

router = Router()


@router.post("/upload", response=List[ImageResponse])
def upload_image(request, profileID: UUID, files: List[UploadedFile] = File(...)):
    created_images = []
    for file in files:
        instance = ProfileImage.objects.create(profileID=profileID, file=file)
        created_images.append(
            {"profileID": instance.profileID, "image_url": instance.file.url}
        )

    return created_images


@router.get("/get/{profileID}", response=List[ImageResponse])
def get_profile_image(request, profileID: UUID):
    images = ProfileImage.objects.filter(profileID=profileID)
    return [{"profileID": img.profileID, "image_url": img.file.url} for img in images]
