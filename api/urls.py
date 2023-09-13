from django.urls import path
from .views import register, login, get_online, suggested_friends

urlpatterns = [

    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('online-users/', get_online, name='get-online'),
    path('suggested-friends/<int:user_id>/',
         suggested_friends, name='suggested-friends'),


]
