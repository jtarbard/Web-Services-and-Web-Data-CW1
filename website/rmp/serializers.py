from rest_framework import serializers

from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password"]

        extra_kwargs = {'email': {'required': True, 'allow_blank': False}, 'password': {'required': True, 'allow_blank': False, "write_only": True}}
