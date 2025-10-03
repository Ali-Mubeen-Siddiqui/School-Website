from django.contrib import admin
from  .models import *
from django.contrib.auth.admin import UserAdmin



# Register your models here.
admin.site.register(Contact)



@admin.register(SiteUser)
class CustomUserAdmin(UserAdmin):
    # add your custom fields here, like user_type
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('user_type',)}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff']