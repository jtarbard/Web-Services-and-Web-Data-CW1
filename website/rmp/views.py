from urllib import request
from django.contrib.auth import authenticate, login
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from django.db.models import Avg
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import CustomUser, Module, Professor, Rating
from .serializers import UserSerializer, ModuleSerializer, ProfessorSerializer, RatingSerializer

class UserViewSet(ModelViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class ModuleViewSet(ReadOnlyModelViewSet):

    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def get_queryset(self):
        queryset = Module.objects.all()
        code = self.request.query_params.get('code')
        professor_id = self.request.query_params.get('professor_id')
        semester = self.request.query_params.get('semester')
        year = self.request.query_params.get('year')
        if code is not None:
            queryset = queryset.filter(code=code, professor=professor_id, semester=semester, year=year)
        return queryset

class ProfessorViewSet(ReadOnlyModelViewSet):

    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer


class RatingViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated,]

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def create(self, request):
        request.data._mutable = True
        request.data["user"] = request.user.id
        request.data._mutable = False
        return super().create(request)

    @action(detail=False)
    def view(self, request):
        professors = Professor.objects.values()
        for prof in professors:
            ratings = self.queryset.filter(professor=prof["id"])
            prof["avg"] = ratings.aggregate(Avg("value"))

        return Response(professors)

    @action(detail=True, methods=["GET"])
    def average(self, request, pk=None):
        try:
            moduleCode = request.json["module_code"]
            professor_id = request.json["professor_id"]
            #todo return error on none
            ratings = self.queryset.filter(module_code=moduleCode, professor=professor_id)
            avg = ratings.aggregate(Avg("value"))
            return Response(avg)
        except:
            return Response(error)