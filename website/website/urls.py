from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from rmp.views import UserViewSet, ModuleViewSet, ProfessorViewSet, RatingViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'module', ModuleViewSet)
# router.register("module/<str:code>", ModuleViewSet)
router.register(r'professor', ProfessorViewSet)
router.register(r'rating', RatingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token)
]