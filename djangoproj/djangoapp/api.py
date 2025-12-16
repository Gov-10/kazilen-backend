from django.db.models import Q, QuerySet
from typing_extensions import List
from typing import List, Optional
from ninja import FilterSchema, NinjaAPI, Query, Schema
from django.shortcuts import get_object_or_404
from .models import Customer, Worker, History
from .schemas import CustomerSchema, WorkerSchema, HistorySchema

api = NinjaAPI()


class workerFilter(FilterSchema):
    category: Optional[List[str]] = None
    subcategory: Optional[List[str]] = None

    def filter_category(self, value: List[str]) -> Q:
        category_value = value[0]
        return Q(category=category_value)
    def filter_subcategory(self, value: List[str]) -> Q:
        subcategory_value = value[0]
        return Q(subcategory__contains=subcategory_value)

@api.get("/worker", response=List[WorkerSchema])
def getAllWorker(request):
    return Worker.objects.all()


# @api.get("/worker/{name}", response=WorkerSchema)
# def getSingleWorker(request, name: str):
#     worker = get_object_or_404(Worker, name=name)
#     # return worker


@api.get("/filterworker", response=List[WorkerSchema])
def getFilterWorker(request, filter: workerFilter = Query(...)):
    workers = Worker.objects.all();
    workers = filter.filter(workers)
    # if filter.category:
    #     workers = workers.filter(category=filter.category)
    # if filter.subcategory:
    #     workers = workers.filter(subcategory=filter.subcategory)
    return workers
