from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=500, blank=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    added_on = models.DateTimeField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def disable_product(self):
        self.is_active = False
        self.save()

    def enable_product(self):
        self.is_active = True
        self.save()