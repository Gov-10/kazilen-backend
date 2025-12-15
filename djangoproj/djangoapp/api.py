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
    match field:
        case "NM":
            workers = Worker.objects.get(name=value)
        case "JP":
            workers = Worker.objects.get(jobProfile=value)
        case "LC":
            workers = Worker.objects.get(location=value)
        case _:
            return
    return workers
