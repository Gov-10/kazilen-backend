from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/signal/<str:client_id>/", consumers.WorkerStatusConsumer.as_asgi()),
]
