# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'is_staff', 'is_active']
    ordering = ['email']
    search_fields = ['email', 'username']

admin.site.register(CustomUser, CustomUserAdmin)
