from django.db import models


class worker(models.Model):
    name = models.CharField(
        max_length=100,
    )
    address = models.CharField(
            max_length= 500,
            )
    phoneNo = models.CharField(
            max_length=15,
            unique = True, 
            )
    jobProfile = models.CharField(
            max_length=250,
            )
