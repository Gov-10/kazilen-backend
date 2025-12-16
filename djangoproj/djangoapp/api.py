from django.db.models import Q, QuerySet
from typing_extensions import List
from typing import List, Optional
from ninja import NinjaAPI, Query, Schema
from django.shortcuts import get_object_or_404
from .models import Customer, Worker, History
from .schemas import CustomerSchema, WorkerSchema, HistorySchema

api = NinjaAPI()


class workerFilter(Schema):
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
def getFilterWorker(request, filter: Query[workerFilter]):
    workers: QuerySet[Worker] = Worker.objects.all();
    q = filter.get_filter_expression()
    if filter.category:
        workers = workers.filter(category=filter.category)
    if filter.subcategory:
        workers = workers.filter(subcategory=filter.subcategory)
    return workers
