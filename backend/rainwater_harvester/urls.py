"""
URL configuration for rainwater_harvester project.
"""

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Smart Rainwater Harvester API")

urlpatterns = [
    path('', home),  # Home page
    path('admin/', admin.site.urls),
    path('api/', include('rainwater_harvester.api.urls')),
]
