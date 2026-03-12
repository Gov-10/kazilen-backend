"""
ASGI config for djangoproj project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import djangoapp.routing
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoproj.settings")

django_asgi_application = get_asgi_application()
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),

        "websocket": AuthMiddlewareStack(
            URLRouter(
                your_app.routing.websocket_urlpatterns
            )
        ),
    }
)
