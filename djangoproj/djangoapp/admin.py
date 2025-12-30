from django.contrib import admin
from .models import Customer, Worker, History
admin.site.register(Customer)
admin.site.register(Worker)
admin.site.register(History)
