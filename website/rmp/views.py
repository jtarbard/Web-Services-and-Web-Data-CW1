from django.contrib.auth import authenticate, login
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import CustomUser, Module, Professor, Rating
from .serializers import UserSerializer, ModuleSerializer, ProfessorSerializer, RatingSerializer

class UserViewSet(ModelViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class ModuleViewSet(ReadOnlyModelViewSet):

    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

class ProfessorViewSet(ReadOnlyModelViewSet):

    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

class RatingViewSet(ModelViewSet):

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer