import uuid
import os
from django.db import models
from django.core.files.storage import storages

def uploadToUUID(instance, filename):
    ext = filename.split('.')[-1]
    filename =  f"{uuid.uuid4()}.{ext}"
    return os.path.join("images", str(instance.profileID), filename)

class ProfileImage(models.Model):
    profileID = models.IntegerField(db_index=True)
    file = models.ImageField(upload_to = uploadToUUID,
                             storage=storages["minio"])
    uploadedAT = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return f"Iamge {self.profileID}"
