import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_sharing.settings')
django.setup()

import subscription.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            subscription.routing.websocket_urlpatterns
        )
    ),
})
