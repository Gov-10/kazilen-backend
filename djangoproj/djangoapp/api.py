from typing_extensions import List
from typing import List
from ninja import NinjaAPI
from django.shortcuts import get_object_or_404
from .models import Customer, Worker, History
from .schemas import CustomerSchema, WorkerSchema, HistorySchema

api = NinjaAPI()


@api.get("/worker", response=List[WorkerSchema])
def getAllWorker(request):
    return Worker.objects.all()


# @api.get("/worker/{name}", response=WorkerSchema)
# def getSingleWorker(request, name: str):
#     worker = get_object_or_404(Worker, name=name)
#     # return worker

@api.get("/filterworker", response=List[WorkerSchema])
def getFilterWorker(request, value: str, field: str = "ALL"):
    match field:
        case "NM":
            workers = Worker.objects.filter(name=value)
        case "JP":
            workers = Worker.objects.filter(jobProfile=value)
        case "LC":
            workers = Worker.objects.filter(address=value)
        case "ALL":
            workers = Worker.objects.all()
        case _:
            return
    return workers
