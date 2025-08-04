from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,"index.html")

def login(request):
    return render(request,"login.html")

def login_view(request):
    pass

def about(request):
    return render(request, "about.html")

def faculty(request):
    return render(request, "faculty.html")

def campus(request):
    return render(request, "campus.html")

def programs(request):
    return render(request, "programs.html")

def admissions(request):
    return render(request, "admissions.html")

def examinations(request):
    return render(request, "examinations.html")

def contact(request):
    return render(request, "contact.html")

