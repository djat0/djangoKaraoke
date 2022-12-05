"""
ASGI config for karaoke project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import karaokey.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "karaoke.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        'websocket': AuthMiddlewareStack(
            URLRouter(
                karaokey.routing.websocket_urlpatterns
            )
        )
    }
)
