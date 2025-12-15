from typing_extensions import List
from typing import List
from ninja import NinjaAPI
from django.shortcuts import get_object_or_404
from .models import Customer, Worker, History
from .schemas import CustomerSchema, WorkerSchema, HistorySchema

api = NinjaAPI()


@api.get("/workers", response=List[WorkerSchema])
def getAllWorker(request):
    return Worker.objects.all()


@api.get("/worker/{name}", response=WorkerSchema)
def getSingleWorker(request, name: str):
    worker = get_object_or_404(Worker, name=name)
    return worker


@api.get("/getworkerList/{filer}/{value}", response=[WorkerSchema])
def getWorkerList(request, filter: str, value: str):
    match filter:
        case "name":
            workers = Worker.objects.get(name=value)
        case "jobProfile":
            workers = Worker.objects.get(jobProfile=value)
        case "rating":
            workers = Worker.objects.get(rating=value)
        case "location":
            workers = Worker.objects.get(location=value)
        case _:
            return 
    return workers
