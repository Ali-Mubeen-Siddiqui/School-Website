
from django.urls import path,include
from . import views

urlpatterns = [
    
    path('', views.index,name="home"),
    path('login/', views.login,name="login"),
    path('loging/', views.login_view,name="loging"),

    
    path('vision/', views.vision, name="vision"),
    path('faculty/', views.faculty, name="faculty"),
    path('campus/', views.campus, name="campus"),
    path('programs/', views.programs, name="programs"),
    path('admissions/', views.admissions, name="admissions"),
    path('examinations/', views.examinations, name="examinations"),

    path('contact/', views.contact, name="contact"),
    path('contact_view/', views.contact_view,name="contact_view"),

    path('gallery/', views.gallery, name="gallery"),
   

]
