from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumers import ChatSocketConsumer

websocket_urlpatterns = [
    path('ws/send/', ChatSocketConsumer.as_asgi(), name='ChatSocketConsumer'),
]

application = ProtocolTypeRouter(
    {
        "websocket": URLRouter(
            websocket_urlpatterns
        ),
    }
)
