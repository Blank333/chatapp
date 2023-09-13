from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumers import ChatSocketConsumer

websocket_urlpatterns = [
    path('api/chat/send/', ChatSocketConsumer.as_asgi(),
         name='ChatSocketConsumer'),
]
