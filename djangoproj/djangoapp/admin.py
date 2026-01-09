from django.contrib import admin
from .models import Customer, Worker, History
admin.site.register(Customer)
admin.site.register(History)

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    readonly_fields=('id',)
    fields = ('id', 'name', 'address', 'phoneNo', 'imageURL', 'category', 'subcategory', 'rating', 'price', 'description')
