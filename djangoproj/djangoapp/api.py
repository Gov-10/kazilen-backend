from django.db.models import Q, QuerySet
from typing_extensions import List
from typing import List, Optional
from ninja import FilterSchema, NinjaAPI, Query, Schema
from django.shortcuts import get_object_or_404
from .models import Customer, Worker, History
from .schemas import CustomerSchema, WorkerSchema, HistorySchema

api = NinjaAPI()


class workerFilter(FilterSchema):
    category: Optional[List[str]]
    subcategory: Optional[List[str]]


@api.get("/worker", response=List[WorkerSchema])
def getAllWorker(request):
    return Worker.objects.all()


# @api.get("/worker/{name}", response=WorkerSchema)
# def getSingleWorker(request, name: str):
#     worker = get_object_or_404(Worker, name=name)
#     # return worker


@api.get("/filterworker", response=List[WorkerSchema])
def getFilterWorker(
    request,
    category: Optional[str] = Query(None),
    subcategory: Optional[str] = Query(None),
):
    filters = Q()
    if category:
        filters &= Q(category=category)
    if subcategory:
        filters &= Q(subcategory=subcategory)
    workers = Worker.objects.filter(filters)
    return workers
