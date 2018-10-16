from django.urls import path
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    
    path('reception', views.reception, name="reception"),
    path('reception/ajax/<int:id>', views.autocomplete, name="autocomplete"),
    path('reception/ajax/load-doctors', views.load_doctors, name='ajax_load_doctors'),
]

