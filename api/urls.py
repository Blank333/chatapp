from django.urls import path
from .views import register, login, get_online

urlpatterns = [

    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('online-users/', get_online, name='get_online'),

    # TODO

    # path('suggested-friends/', api_home, name='api_home'),
]

# Get online users: GET /api/online-users/
# Recommended friends: GET /api/suggested–friends/<user_id>

# Start a chat: POST /api/chat/start/
# Send a message: WEBSOCKET /api/chat/send/
