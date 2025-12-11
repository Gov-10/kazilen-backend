from typing_extensions import List
from typing import List
from ninja import NinjaAPI
from django.shortcuts import get_object_or_404
from .models import Customer, Worker, History
from .schemas import CustomerSchema, WorkerSchema, HistorySchema
api = NinjaAPI()

@api.get("/worker", response=List[WorkerSchema])
def getAllWorker(request):
    #workers = get_object_or_404(**request)
    workers = Worker.objects.all()
