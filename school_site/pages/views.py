from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Contact,Admission

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
    if request.method != "POST":
        return render(request, "admission.html")

    try:
        child_full_name = request.POST.get("child_full_name")
        father_name = request.POST.get("father_name")
        mother_name = request.POST.get("mother_name")
        admission_class = request.POST.get("admission_class")
        present_school = request.POST.get("present_school")
        board = request.POST.get("board")
        mobile_no = request.POST.get("mobile_no")
        address = request.POST.get("address")

        error = validate_admission(child_full_name,father_name,mother_name,admission_class,present_school,board,mobile_no,address)
        if error:
            messages.error(request, error)
            return redirect("admissions")
        
        new_admission = Admission(child_full_name=child_full_name,father_name=father_name,mother_name=mother_name,admission_class=admission_class,present_school=present_school,board=board,mobile_no=mobile_no,address=address)
        new_admission.save()
        messages.success(request, "Thank you! Your admission has been submitted.")
        return redirect("admissions")

    except Exception as e:
        pass

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

        error = validate_contact(name,email,subject,message)
        if error:
            messages.error(request, error)
            return redirect("contact")

        new_contact = Contact(name=name,email=email,subject=subject,message=message)
        new_contact.save()
        messages.success(request, "Thank you! Your message has been sent.")
        return redirect("contact")


    except Exception as e:
        messages.error(request, "Sorry, something went wrong. Please try again.")
        return redirect("contact")
        

def validate_contact(name,email,subject,message):
    if not name or not email or not subject or not message:
        return "All fields are required"
    if name.strip() == "" or email.strip() == "" or subject.strip() == "" or message.strip() == "":
        return "All fields are required"
    # The original condition used 'or' incorrectly, causing it to always return "Invalid email format"
    # It should check if the email DOES NOT end with ANY of the allowed domains.
    # This means if it doesn't end with gmail AND it doesn't end with yahoo AND it doesn't end with hotmail.
    if not (email.endswith("@gmail.com") or email.endswith("@yahoo.com") or email.endswith("@hotmail.com")):
        return "Invalid email format"
    if len(name) > 100:
        return "Name must be less than 100 characters"
    if len(subject) > 100:
        return "Subject must be less than 100 characters"
    if len(message) > 500:
        return "Message must be less than 500 characters"
    
    return None


def validate_admission(child_full_name,father_name,mother_name,admission_class,present_school,board,mobile_no,address):
    if not child_full_name or not father_name or not mother_name or not admission_class or not present_school or not board or not mobile_no or not address:
        return "All fields are required"
    if len(child_full_name) > 100:
        return "Child's full name must be less than 100 characters"
    if len(father_name) > 100:
        return "Father's name must be less than 100 characters"
    if len(mother_name) > 100:
        return "Mother's name must be less than 100 characters"
    if len(admission_class) > 50:
        return "Admission class must be less than 50 characters"
    if len(present_school) > 100:
        return "Present school must be less than 100 characters"
    if len(board) > 20:
        return "Board must be less than 20 characters"
    if len(mobile_no) > 20:
        return "Mobile number must be less than 20 characters"
    if len(address) > 250:
        return "Address must be less than 250 characters"
    return None