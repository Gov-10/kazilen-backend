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

@api.get("/workerfilter/{filter}", response=List[WorkerSchema])
def getFilterWorker(request, filter: str):
    field, value = filter.split("&")
    print(field, value)
    match field:
        case "NM":
            workers = Worker.objects.filter(name=value)
        case "JP":
            workers = Worker.objects.filter(jobProfile=value)
        case "LC":
            workers = Worker.objects.filter(address=value)
        case _:
            return
    return workers
