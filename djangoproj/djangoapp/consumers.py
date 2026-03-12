from channels.generic.websocket import AsyncWebsocketConsumer
import json
class WorkerStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("workers", self.channel_name)
        await self.accept()
    async def disconnect(self):
        await self.channel_layer.group_discard("workers", self.channel_name)
    async def worker_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))

