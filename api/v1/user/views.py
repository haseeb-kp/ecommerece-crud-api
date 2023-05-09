from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from api.v1.user.serializers import *
from django.contrib.auth import get_user_model
from app.models import Product
import re
from utils.exception_handler import handle_exceptions
from django.shortcuts import get_object_or_404
from datetime import date 
import datetime
from django.utils import timezone


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


class ProductListView(ListCreateAPIView):
    """
    View for listing and creating products for a user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Exception as e:
            return handle_exceptions(e)


class UserEditProfileView(UpdateAPIView):
    """
    View for user edit.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        #updating user data
        try:
            user = self.get_object()
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return handle_exceptions(e)
            

class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class ActivateDeactivateProductView(UpdateAPIView):
    """
    View for activating or deactivating a product.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get_object(self):
        product_id = self.kwargs.get('pk')
        product = get_object_or_404(Product, id=product_id, user=self.request.user)
        return product

    def patch(self, request, *args, **kwargs):
        try:
            product = self.get_object()
            if product.is_active:
                # Check if product was added before 2 months
                two_months_ago = date.today() - datetime.timedelta(days=60)
                if two_months_ago < product.added_on :
                    return Response({"error": "Cannot deactivate product within 2 months of adding."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    product.disable_product()
                    return Response({"message": "Product has been deactivated."})
            else:
                product.enable_product()
                return Response({"message": "Product has been activated."})
        except Exception as e:
            return handle_exceptions(e)





