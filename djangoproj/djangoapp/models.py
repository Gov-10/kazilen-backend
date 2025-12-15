from enum import unique
from django.db import models
import phonenumber_field
from phonenumber_field.modelfields import PhoneNumberField


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
    class JobProfiles(models.TextChoices):
        vehicle = "vehicle", "mechanic"
        health = "health", "doctor"
        carpenter = "carpenter", "carpenter"
        electrician = "electrician", "electrician"
        home = "home", "home cleaning/services"
        appliance = "appliance", "electronic device"
        labour = "labour", "manual labour"

    name = models.CharField(
        max_length=100,
    )
    address = models.CharField(
        max_length=500,
    )
    phoneNo = PhoneNumberField(null=False, blank=False, unique=True)
    jobProfile = models.CharField(
        max_length=30,
        choices=JobProfiles.choices,
        default=JobProfiles.labour,
    )

    rating = models.FloatField()

    price = models.DecimalField(max_digits=11, decimal_places=3)

    discription = models.CharField(max_length=200)
