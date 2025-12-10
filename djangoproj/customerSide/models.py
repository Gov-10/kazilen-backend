from django.db import models
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


class history(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="historyRecords",
    )
    action = models.CharField(max_length=30)
    timestmp = models.DateTimeField(auto_now=True)
