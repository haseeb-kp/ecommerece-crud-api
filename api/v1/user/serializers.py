from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from app.models import Product
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=30, validators=[validate_email])
    name = serializers.CharField(max_length=30)
    phone_number = serializers.CharField(max_length=15)

    def validate_name(self, name):
        if not re.match("^[a-zA-Z ]*$", name):
            raise serializers.ValidationError("Name can only contain alphabets and spaces.")
        return name

    def validate_phone_number(self, phone_number):
        if not re.match("^[0-9]*$", phone_number):
            raise serializers.ValidationError("Phone number can only contain digits.")
        return phone_number

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password','phone_number']
        extra_kwargs = {'password': {'write_only': True}}

