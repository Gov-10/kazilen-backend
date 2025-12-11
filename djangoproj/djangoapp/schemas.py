from ninja import ModelSchema
from .models import Customer, Worker, History

class CustomerSchema(ModelSchema):
    phoneNo: str
    class Meta:
        model = Customer
        fields = '__all__'

class WorkerSchema(ModelSchema):
    phoneNo: str
    class Meta:
        model = Worker
        fields = '__all__'

class HistorySchema(ModelSchema):
    class Meta:
        model = History
        fields = '__all__'

