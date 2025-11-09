from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class SiteUser(AbstractUser):
    USER_TYPE = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE, default='student')




# model for contact us page
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=500)


    def __str__(self):
        return f"{self.name} - {self.subject}"

class Admission(models.Model):
    BOARD_CHOICES = (
        ('CISCE', 'CISCE'),
        ('CBSE', 'CBSE'),
        ('State Board', 'State Board'),
    )

    child_full_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    admission_class = models.CharField(max_length=50)
    present_school = models.CharField(max_length=100)
    board = models.CharField(max_length=20, choices=BOARD_CHOICES)
    mobile_no = models.CharField(max_length=20)
    address = models.TextField(max_length=250)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Admission for {self.child_full_name} ({self.admission_class})"



class Album(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    class Meta:
        ordering = ['-date']
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'
    
    def get_media_count(self):
        return self.media_items.count()

    def __str__(self):
        return self.title

def get_upload_path(instance, filename):
    """Organize uploads by album and media type"""
    if instance.media_type == 'Image':
        return f'gallery/{instance.album.id}/images/{filename}'
    else:
        return f'gallery/{instance.album.id}/videos/{filename}'

class AlbumMedia(models.Model):
    type_choices = (
        ('Image', 'Image'),
        ('Video', 'Video')
    )
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='media_items')
    media_type = models.CharField(max_length=10, choices=type_choices)
    
    # File field that handles both images and videos
    file = models.FileField(upload_to=get_upload_path)
    caption = models.CharField(max_length=200, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.media_type} - {self.album.title}"
    