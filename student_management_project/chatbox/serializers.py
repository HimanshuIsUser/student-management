import re

from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from chatbox.models import *

class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()

        fields = (
            'id', 'name','surname','password', 'email', 'date_joined', 'last_login')
        read_only_fields = ()


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'name', 'email', 'password',)
        extra_kwargs = {'password': {'write_only': True}}
        extra_kwargs = {'name': {'required': True, 'allow_blank': False},
}

    def validate_password(self, password):
        if len(password) < 8 or len(password) > 15:
            raise serializers.ValidationError('Password 8-15 Characters')
        return password

    def create(self, validated_data):
        
        email_cleaned = validated_data['email'].lower()

        user = get_user_model().objects.create_user(
            email_cleaned, validated_data['password'], name=validated_data['name'])

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = ["email", "password"]

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

class StudentdetailsSerializer(ModelSerializer):
    class Meta:
        model = StudentDetails

        fields = (
            'name','surname','no_of_update',
        )
        read_only_fields = ()