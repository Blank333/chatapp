from django.contrib import admin
from django.urls import path, include
import api.urls as apiURLs
import chat.urls as chatURLs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(apiURLs)),
    path('api/chat/', include(chatURLs)),

]
