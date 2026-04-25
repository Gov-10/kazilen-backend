from django.db import models
import os
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField
from django.core.files.storage import storages
import uuid


def upload_worker_image(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("workers", str(instance.id), filename)


class Customer(models.Model):
    gender = [("M", "Male"), ("F", "Female"), ("O", "Others"), ("N", "rather not say")]
    name = models.CharField(
        max_length=100,
        verbose_name="fullName",
    )
    phoneNo = PhoneNumberField(unique=True)
    email = models.EmailField(
        max_length=256,
        unique=True,
    )
    gender = models.CharField(max_length=100, choices=gender, default=gender[-0])
    dob = models.DateField(null=True, blank=True)

    work_id = models.UUIDField(null=True, primary_key=False, blank=True, editable=True)
    temp_id = models.UUIDField(null=True, primary_key=False, blank=True, editable=True)

    is_online = models.BooleanField(default=False)

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    def __str__(self):
        return f"id : {self.id}"


subcategories = [
        "consult",
        "hourly",
        "fan-install",
        "fan-repair",
        "light",
        "home-wiring",
        "switch-install",
        "switch-mcb",
        "switch-repair",
        "invereter-install",
        "invereter-maintainance",
        "cooler-repair",
        "motor-rewinding",
    ]
def initialize_items():
    new_data = []
    for cate in subcategories:
        new_data.append({
            "name" : cate,
            "visible": False,
            "price": 120,
            "details": "",
        })
    return new_data

class Worker(models.Model):
    gender = [("M", "Male"), ("F", "Female"), ("O", "Others"), ("N", "rather not say")]

    name = models.CharField(
        max_length=100,
    )
    address = models.CharField(
        max_length=500,
    )
    phoneNo = PhoneNumberField(unique=True)
    imageURL = models.ImageField(
        upload_to=upload_worker_image,
        storage=storages["minio"],
        null=True,
        blank=True,
        editable=True,
    )
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    is_working = models.BooleanField(default=False, editable=True)
    is_online = models.BooleanField(default=False, editable=True)

    work_id = models.UUIDField(null=True, primary_key=False, blank=True, editable=True)
    temp_id = models.UUIDField(null=True, primary_key=False, blank=True, editable=True)

    rating = models.FloatField(default=0, editable=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=gender, default=gender[-1])


    location = models.CharField(null=True, default="", editable=True)

    description = models.CharField(max_length=200, blank=True, null=True, editable=True)
    categories = models.CharField(default='electrician')
    sub_categories = models.JSONField(default=initialize_items, editable=True)

    
    def __str__(self):
        return f"{self.name}-{self.id}"


class History(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="historyRecords",
    )
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    action = models.CharField(max_length=30)
    timestmp = models.DateTimeField(auto_now=True)
    is_finished = models.BooleanField(null=False, default=False)

    def __str__(self):
        return f"{self.customer.name}:{self.action}:{self.worker}->{self.timestmp}"
