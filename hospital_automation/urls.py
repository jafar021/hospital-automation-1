from django.urls import path
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    
    path('reception', views.index, name="reception"),
]

