from ninja import ModelSchema, Schema
from djangoapp.models import Worker


class phonePayload(Schema):
    phone: str

class CreateWorkerSchema(ModelSchema):
    phoneNo: str 
    imageURL: str
    class Meta:
        model = Worker
        fields = "__all__"
    @staticmethod
    def resolve_phoneNo(obj):
        if not obj.phoneNo:
            return None
        return str(obj.phoneNo)
