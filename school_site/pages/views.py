from django.shortcuts import render,redirect
from django.contrib import messages
from asgiref.sync import sync_to_async
from .models import Contact,Admission,Album,AlbumMedia
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404


# Create your views here.

async def index(request):
    return render(request,"index.html")

async def login(request):
    return render(request,"login.html")



async def vision(request):
    return render(request, "vision.html")

async def faculty(request):
    return render(request, "faculty.html")

async def campus(request):
    return render(request, "campus.html")

async def programs(request):
    return render(request, "programs.html")

async def admissions(request):
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
        
        # Use sync_to_async for database operations
        new_admission = Admission(child_full_name=child_full_name,father_name=father_name,mother_name=mother_name,admission_class=admission_class,present_school=present_school,board=board,mobile_no=mobile_no,address=address)
        save_func = sync_to_async(new_admission.save, thread_sensitive=True)
        await save_func()
        messages.success(request, "Thank you! Your admission has been submitted.")
        return redirect("admissions")

    except Exception as e:
        pass

async def examinations(request):
    return render(request, "examinations.html")

async def contact(request):
    return render(request, "contact.html")




# ---------- GALLERY VIEW ----------
async def gallery(request):
    try:
        # ORM queries
        albums_qs = await sync_to_async(lambda: Album.objects.filter(is_active=True).order_by('-date'))()
        media_qs = await sync_to_async(lambda: AlbumMedia.objects.order_by('-uploaded_at'))()
        paginator = await sync_to_async(Paginator)(media_qs, 2)
        page_obj = await sync_to_async(paginator.get_page)(1)

        context = {
            'albums': albums_qs,
            'media_items': page_obj,
        }

        # render() is sync
        response = await sync_to_async(render)(request, "gallery/gallery.html", context)
        return response

    except Exception as e:
        # messages.error and redirect are sync too
        await sync_to_async(messages.error)(request, f"Error loading gallery: {e}")
        print(e)
        return await sync_to_async(redirect)("home")

        
# ---------- SPECIFIC ALBUM MEDIA VIEW ----------
async def album_media(request, slug):
    try:
        # ORM
        album = await sync_to_async(lambda: get_object_or_404(Album, slug=slug))()
        media_qs = await sync_to_async(lambda: list(album.media_items.all().order_by('-uploaded_at')))()

        # Pagination
        paginator = await sync_to_async(Paginator)(media_qs, 2)
        page_obj = await sync_to_async(paginator.get_page)(1)

        context = {
            'album': album,
            'media_items': page_obj,
        }

        # render() is sync
        response = await sync_to_async(render)(request, "gallery/partials/media_grid.html", context)
        return response

    except Exception as e:
        await sync_to_async(messages.error)(request, f"Error loading album: {e}")
        return await sync_to_async(redirect)("gallery")

    except Exception as e:
        messages.error(request, f"Error loading album: {e}")
        return redirect("gallery")

# ---------- PAGINATION FOR ALL MEDIA ----------
async def gallery_page(request, page):
    try:
        media_qs = await sync_to_async(lambda: list(AlbumMedia.objects.all().order_by('-uploaded_at')))()

        paginator = await sync_to_async(Paginator)(media_qs, 2)
        page_obj = await sync_to_async(paginator.get_page)(page)

        response = await sync_to_async(render)(request, "gallery/partials/media_grid.html", {"media_items": page_obj})
        return response

    except Exception as e:
        await sync_to_async(messages.error)(request, f"Error loading page: {e}")
        return await sync_to_async(redirect)("gallery")


async def login_view(request):
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


async def contact_view(request):
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

        # Use sync_to_async for database operations
        new_contact = Contact(name=name,email=email,subject=subject,message=message)
        save_func = sync_to_async(new_contact.save, thread_sensitive=True)
        await save_func()
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