from django.db.models import QuerySet
from typing_extensions import List
from typing import List, Optional
from ninja import NinjaAPI, Query
from django.shortcuts import get_object_or_404
from .models import Customer, Worker, History
from .schemas import CustomerSchema, WorkerSchema, HistorySchema

api = NinjaAPI()


class workerFilter(Query):
    category: Optional[str] = None
    subcategory: Optional[str] = None


@api.get("/worker", response=List[WorkerSchema])
def getAllWorker(request):
    return Worker.objects.all()


# @api.get("/worker/{name}", response=WorkerSchema)
# def getSingleWorker(request, name: str):
#     worker = get_object_or_404(Worker, name=name)
#     # return worker


@api.get("/filterworker", response=List[WorkerSchema])
def getFilterWorker(request, filter: workerFilter):
    workers: QuerySet[Worker] = Worker.objects.all();
    if filter.category:
        workers = workers.filter(category=filter.category)
    return workers
