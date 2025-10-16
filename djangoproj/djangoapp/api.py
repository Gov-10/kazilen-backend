from ninja import NinjaAPI
api = NinjaAPI()

@api.get("/hello")
async def hello(request):
    return {"message": "hello"}