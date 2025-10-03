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