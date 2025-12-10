from ninja import ModelSchema
from .models import Customer, Worker, History

class CustomerSchema(ModelSchema):
    class meta:
        model = Customer
        fields = '__all__'

class WorkerSchema(ModelSchema):
    class meta:
        model = Worker
        fields = '__all__'

class HistorySchema(ModelSchema):
    class meta:
        model = History
        fields = '__all__'

