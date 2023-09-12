from django.urls import path
from .views import start_chat

urlpatterns = [
    path('start/', start_chat, name='start_chat'),
]