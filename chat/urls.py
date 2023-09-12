from django.urls import path
from .views import start_chat
from .consumers import ChatSocketConsumer
urlpatterns = [
    path('start/', start_chat, name='start_chat'),
    path('send/', ChatSocketConsumer.as_asgi(), name='ChatSocketConsumer'),
]
