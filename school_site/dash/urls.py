from django.contrib import admin
from django.urls import path
from . import views

app_name = "student"

urlpatterns = [
    
    path('dashboard/', views.login_view,name="dashboard"),
]
