from django.shortcuts import render
from rest_framework import viewsets

from .models import CustomUser
from .serializers import CustomUserCreationSerializer

class RegisterViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = CustomUserCreationSerializer