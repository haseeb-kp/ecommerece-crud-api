from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from api.v1.user.serializers import *
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from app.models import Product
from rest_framework.exceptions import ParseError
import re
from utils.exception_handler import handle_exceptions

User = get_user_model()

class UserSignupView(CreateAPIView):
    """
    View for user signup.
    """
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # overriding default create function to use custom create_user function.
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            phone_number = serializer.validated_data['phone_number']
            user = User.objects.create_user(email=email, password=password, name=name,phone_number=phone_number)
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return handle_exceptions(e)


class AddProductView(CreateAPIView):
    """
    View for adding a product by a user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Exception as e:
            return handle_exceptions(e)
            



