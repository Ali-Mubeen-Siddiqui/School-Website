from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Contact

# Create your views here.

def index(request):
    return render(request,"index.html")

def login(request):
    return render(request,"login.html")


def vision(request):
    return render(request, "vision.html")

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

def gallery(request):
    return render(request, "gallery.html")

def login_view(request):
    # Ensure the view always returns a response
    if request.method != "POST":
        return redirect("login")

    name = request.POST.get("username")
    password = request.POST.get("password")
    user_type = request.POST.get('user_type')

    # Simple routing based on selected user type
    if user_type == "student":
        # dash app exposes name="dashboard" at path student/dashboard/
        return redirect("student:dashboard")

    if user_type == "staff":             
        # Placeholder: send staff somewhere sensible; fallback to home for now
        return redirect("staff")

    # Fallback if user_type missing/unknown
    return redirect("login")


def contact_view(request):
    if request.method != "POST":
        return redirect("contact")
    
    try:
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        new_contact = Contact(name=name,email=email,subject=subject,message=message)
        new_contact.save()
        messages.success(request, "Thank you! Your message has been sent.")
        return redirect("contact")


    except Exception as e:
        messages.error(request, "Sorry, something went wrong. Please try again.")
        return redirect("contact")
        