from django.contrib import admin
from django.urls import path
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from rmp.views import CustomUserViewSet

router = DefaultRouter()
router.register(r'student', CustomUserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]