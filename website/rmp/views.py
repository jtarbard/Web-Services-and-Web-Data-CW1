from urllib import request
from django.contrib.auth import authenticate, login
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from django.db.models import Avg
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action

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

    permission_classes = [IsAuthenticated,]

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    @action(detail=False)
    def view(self, request):
        professors = Professor.objects.values()
        for prof in professors:
            ratings = self.queryset.filter(professor=prof["id"])
            prof["avg"] = ratings.aggregate(Avg("value"))

        return Response(professors)
