from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .serializers import CustomUserSerializer
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    serializer = CustomUserSerializer
    model = CustomUser
    list_display = ["email", "username",]

admin.site.register(CustomUser, CustomUserAdmin)