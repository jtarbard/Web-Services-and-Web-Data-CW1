from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .serializers import CustomUserCreationSerializer
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    serializer = CustomUserCreationSerializer
    model = CustomUser
    list_display = ["email", "username",]

admin.site.register(CustomUser, CustomUserAdmin)