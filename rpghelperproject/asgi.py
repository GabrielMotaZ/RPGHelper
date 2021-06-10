"""
ASGI config for rpghelperproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.http import AsgiHandler
import helper_app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rpghelperproject.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": AsgiHandler(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            helper_app.routing.websocket_urlpatterns
        )
    ),
})
