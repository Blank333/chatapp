from django.urls import path
from .views import start_chat, send

urlpatterns = [
    path('start/', start_chat, name='start_chat'),
    path('send/', send, name='send'),

]
