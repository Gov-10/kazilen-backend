from typing_extensions import List
from typing import List
from ninja import NinjaAPI
from django.shortcuts import get_object_or_404
from .models import Customer, Worker, History
from .schemas import CustomerSchema, WorkerSchema, HistorySchema
api = NinjaAPI()

@api.get("/workers", response=List[WorkerSchema])
def getAllWorker(request):
    #workers = get_object_or_404(**request)
    return Worker.objects.all()

@api.get("/worker/{name}", response=WorkerSchema)
def getSingleWorker(request, name: str):
        worker = get_object_or_404(Worker, jobProfile=name)
        return worker

@api.get("/worker/jobProfile/{filter}", response=List[WorkerSchema])
def getWorkersByJob(request, filter:str):
    worker = get_object_or_404(Worker, jobProfile=filter)
    return worker
