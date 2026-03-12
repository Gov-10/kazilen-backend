from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
channel_layer= get_channel_layer()
def worker_update(worker):
    async_to_sync(channel_layer.group_send)(
        "workers",
        {"type": "worker.update", "data": {"id": worker.id, "status": worker.is_live}}
            )
