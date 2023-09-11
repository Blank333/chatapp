from django.contrib import admin
from django.urls import path, include
import api.urls as apiURLs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(apiURLs)),
]
