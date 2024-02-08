from django.db import models

# Create your models here.
import uuid
from django.contrib.auth.models import AbstractUser


class UserProfiles(AbstractUser):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
    GENDER_IN_CHOICES = [
        (MALE, "Male"),
        (FEMALE, "Female"),
        (OTHER, "Other"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=120, null=True, blank=True)
    username = models.CharField(max_length=120, null=True, blank=True)
    last_name = models.CharField(max_length=120, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=20, blank=True, null=True, unique=True)
    gender = models.CharField(
        max_length=6, choices=GENDER_IN_CHOICES, null=True, blank=True)
    country = models.CharField(max_length=120, null=True, blank=True)
    profile = models.URLField(max_length=255, blank=True)
    customer_omise_id = models.CharField(max_length=255, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        UserProfiles, on_delete=models.SET_NULL, null=True)
    fullname = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    detail_address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    image = models.URLField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    # quantity = models.IntegerField(blank=True, null=True)
    # size = models.CharField(max_length=255, blank=True, null=True)
    # color = models.CharField(max_length=255, blank=True, null=True)
    # c


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        UserProfiles, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class ShoppingCart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        UserProfiles, on_delete=models.SET_NULL, null=True)
    total = models.FloatField(blank=True, null=True,default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
