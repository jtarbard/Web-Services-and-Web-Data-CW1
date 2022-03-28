from rest_framework.serializers import ModelSerializer

from .models import CustomUser, Module, Professor, Rating

class UserSerializer(ModelSerializer):

    def create(self,validated_data):
            user = CustomUser.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
            return user

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password"]

        extra_kwargs = {'email': {'required': True, 'allow_blank': False}, 'password': {'required': True, 'allow_blank': False, 'allow_null': False, 'write_only': True}}


class ProfessorSerializer(ModelSerializer):

    class Meta:
        model = Professor
        fields = "__all__"


class ModuleSerializer(ModelSerializer):

    professor = ProfessorSerializer(many=True)

    class Meta:
        model = Module
        fields = "__all__"


class RatingSerializer(ModelSerializer):
    
    professor = ProfessorSerializer()
    module = ModuleSerializer()

    class Meta:
        model = Rating
        fields = ["user", "value", "module", "professor"]