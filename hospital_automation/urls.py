from django.urls import path
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('reception/', views.reception, name="reception"),
    path('reception/ajax/<int:id>', views.autocomplete, name="autocomplete")
]
