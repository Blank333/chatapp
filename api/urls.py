from django.urls import path
from .views import api_home

urlpatterns = [


    ## TODO
    
    path('register/', api_home, name='api_home'),
    # path('login/', api_home, name='api_home'),
    # path('online-users/', api_home, name='api_home'),
    # path('suggested-friends/', api_home, name='api_home'),
]

# User registration: POST /api/register/
# User login: POST /api/login/
# Get online users: GET /api/online-users/
# Recommended friends: GET /api/suggested–friends/<user_id>

# Start a chat: POST /api/chat/start/
# Send a message: WEBSOCKET /api/chat/send/
