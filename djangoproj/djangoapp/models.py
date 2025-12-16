from django.db import models
from django.db.models.fields import CharField
from django.utils import choices
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField

class Customer(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="fullName",
    )
    address = models.CharField(max_length=500)
    phoneNo = PhoneNumberField(unique=True)
    email = models.EmailField(
        max_length=256,
        unique=True,
    )


class History(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="historyRecords",
    )
    action = models.CharField(max_length=30)
    timestmp = models.DateTimeField(auto_now=True)


class Worker(models.Model):
    JobProfiles = [
        ("vehicle", "mechanic"),
        ("mechanic", "health"),
        ("doctor", "carpenter"),
        ("carpenter", "electrician"),
        ("electrician", "home"),
        ("home cleaning/services", "appliance"),
        ("electronic device", "labour"),
        ("manual", " labour")
    ]
    SubCategory = (
        ("consult", "be a consultant"),
        ("fixed", "Fixed Charges"),
        ("Book", "Hourly pay")
        )
    name = models.CharField(
        max_length=100,
    )
    address = models.CharField(
        max_length=500,
    )
    phoneNo = CharField(max_length=15, unique=True)
    category = models.CharField(
        max_length=30,
        choices=JobProfiles,
        default=JobProfiles[-1],
    )
    subcategory = MultiSelectField(choices=SubCategory, default=["consultant"], min_choices=1, max_length=20)
    rating = models.FloatField()

    price = models.DecimalField(max_digits=11, decimal_places=3)

    description = models.CharField(max_length=200)
