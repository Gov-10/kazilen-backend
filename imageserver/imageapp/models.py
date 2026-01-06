import uuid
from django.db import models
from django.contrib import admin


def userDirPath(instance, fileName):
    return f'user_{instance.profile.uniqueID}/{fileName}'

class Profile(models.Model):
    uniqueID = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class ProfileImage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to = userDirPath)
    isPrimary = models.BooleanField(default=False)
    uploadedAt = models.DateTimeField(auto_now_add=True)    
