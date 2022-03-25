from django.contrib.auth import authenticate, login
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import CustomUser
from .serializers import CustomUserSerializer

class CustomUserViewSet(ModelViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    # async def post(self, request):

    #     if self.serializer.is_valid():
    #         self.serializer_class.save()
    #         return Response(status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(self.serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)