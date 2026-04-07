from channels.generic.websocket import AsyncWebsocketConsumer
import json
class WorkerStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.group_name = f"worker_{self.user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
    async def disconnect(self):
        await self.channel_layer.group_discard(self.group_name ,self.channel_name)
    async def worker_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))
    async def send_wake(self, event):
        await self.send(text_data=json.dumps({
            "command": "wake" 
            }))
