from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .serializers import UserSerializer
from .models import CustomUser, Module, Professor, Rating

class CustomUserAdmin(UserAdmin):
    serializer = UserSerializer
    model = CustomUser
    list_display = ["email", "username",]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Professor)
admin.site.register(Module)
admin.site.register(Rating)
