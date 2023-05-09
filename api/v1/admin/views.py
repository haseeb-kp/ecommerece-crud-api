from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from api.v1.user.serializers import *
from django.contrib.auth import get_user_model
from app.models import Product
import re
from utils.exception_handler import handle_exceptions

User = get_user_model()


class CustomerListView(ListAPIView):
    """
    View for listing all users except superusers.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return User.objects.filter(is_superuser=False)


class ProductListView(ListAPIView):
    """
    View for listing all products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CustomerDetailView(RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a specific customer.
    """
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

    def partial_update(self, request, *args, **kwargs):
        """ Call the default implementation of partial_update,
        but with the `partial` argument set to True.
        This ensures that the PATCH request will behave as expected."""

        kwargs['partial'] = True
        return super().partial_update(request, *args, **kwargs)



class ProductListAPIView(ListCreateAPIView):
    """
    View for listing and creating products for a specific customer.
    """
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer

    def get_queryset(self):
        # Filter the queryset to only include products for the specified customer
        customer_id = self.kwargs.get('id')
        return Product.objects.filter(user_id=customer_id)

    def perform_create(self, serializer):
        # Set the customer ID on the product before saving
        customer_id = self.kwargs.get('id')
        serializer.save(user_id=customer_id)


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a specific product for a specific customer.
    """
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer

    def get_queryset(self):
        # Filter the queryset to only include products for the specified customer
        customer_id = self.kwargs.get('id')
        return Product.objects.filter(user_id=customer_id)