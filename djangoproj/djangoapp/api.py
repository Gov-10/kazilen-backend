from ninja import NinjaAPI
api = NinjaAPI()

@api.get("/hello")
async def hello():
    return {"message": "hello"}