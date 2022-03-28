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

    permission_classes = [IsAuthenticated,]

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

    permission_classes = [IsAuthenticated,]

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
            prof["avg"]["value__avg"] = round(prof["avg"]["value__avg"])

        return Response(professors)

    @action(detail=False, methods=["post"])
    def average(self, request):
        modules = Module.objects.filter(code=request.data["module_code"], professor=request.data["professor"])
        if modules is None:
            return Response("Module could not be found.")

        module_ids = []
        for module in modules:
            module_ids.append(module.id)

        filtered_ratings = self.queryset.filter(module_id__in=module_ids)
        avg = filtered_ratings.aggregate(Avg("value"))
        professor = Professor.objects.get(id=request.data["professor"])
        data = {
            "avg": round(avg["value__avg"]),
            "module_title": modules[0].title,
            "module_code": modules[0].code,
            "professor_id": professor.id,
            "first_name": professor.first_name,
            "last_name": professor.last_name,
        }
        return Response(data)