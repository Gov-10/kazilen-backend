from django.urls import path
from .consumers import WorkerStatusConsumer

websocket_urlpatterns=[
    path("ws/workers/", WorkerStatusConsumer.as_asgi()),
        ]
