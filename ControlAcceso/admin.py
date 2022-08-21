from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'is_superuser', 'is_staff', 'is_active', 'date_joined')
    
admin.site.register(User, UserAdmin)