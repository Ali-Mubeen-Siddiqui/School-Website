from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    
    path('', views.index,name="home"),
    path('login/', views.login,name="login"),
    path('about/', views.about, name="about"),
    path('faculty/', views.faculty, name="faculty"),
    path('campus/', views.campus, name="campus"),
    path('programs/', views.programs, name="programs"),
    path('admissions/', views.admissions, name="admissions"),
    path('examinations/', views.examinations, name="examinations"),
    path('contact/', views.contact, name="contact"),
]
