from rest_framework.serializers import ModelSerializer

from .models import CustomUser, Module, Professor, Rating

class UserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password"]

        extra_kwargs = {'email': {'required': True, 'allow_blank': False}, 'password': {'required': True, 'allow_blank': False, "write_only": True}}

class ModuleSerializer(ModelSerializer):

    class Meta:
        model = Module
        fields = ["__all__"]

class ProfessorSerializer(ModelSerializer):

    class Meta:
        model = Professor
        fields = ["__all__"]

class RatingSerializer(ModelSerializer):

    class Meta:
        model = Rating
        fields = ["user", "module", "value"]


