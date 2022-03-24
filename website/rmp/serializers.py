from rest_framework import serializers

from .models import CustomUser

class CustomUserCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["username", "email"]
        write_only_fields = ["password"]

        extra_kwargs = {'username': {'required': True}}
        extra_kwargs = {'email': {'required': True}}