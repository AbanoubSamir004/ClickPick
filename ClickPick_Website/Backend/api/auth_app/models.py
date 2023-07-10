from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from djongo.models.fields import ObjectIdField
from bson import ObjectId


class AppUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('An email is required.')

        email = self.normalize_email(email)
        favorite_products = extra_fields.pop('favorite_products', [])  # Remove favorite_products from extra_fields

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.favorite_products = favorite_products  # Assign the provided value
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    email = models.EmailField(max_length=50, unique=True)
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    address = models.CharField(max_length=255)
    favorite_products = models.JSONField(default=list, blank=True)
    reset_password_otp = models.IntegerField(null=True, blank=True)

    # Additional fields for superuser
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'birth_date', 'address']

    objects = AppUserManager()

    class Meta:
        db_table = 'Users_Collection'

    def __str__(self):
        return self.email


