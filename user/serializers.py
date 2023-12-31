from typing import Any, Dict
from rest_framework import serializers
from .models import *
from rolepermissions.roles import assign_role

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login
from django.contrib.auth import password_validation
from django.core import exceptions


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return super().update(instance, validated_data)


class UserProfilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfiles
        fields = "__all__"
        depth = 1
        extra_kwargs = {
            'password': {'write_only': True},

        }


class UserProfilesUpdateSerializer(serializers.Serializer):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
    GENDER_IN_CHOICES = [
        (MALE, "Male"),
        (FEMALE, "Female"),
        (OTHER, "Other"),
    ]
    address_id = serializers.IntegerField(required=True)
    first_name = serializers.CharField(max_length=120, required=False)
    last_name = serializers.CharField(max_length=120, required=False)
    username = serializers.CharField(max_length=120, required=False)
    gender = serializers.ChoiceField(
        choices=GENDER_IN_CHOICES, allow_null=True, allow_blank=True)
    country = serializers.CharField(max_length=120, required=False)
    profile = serializers.URLField(
        max_length=255, required=False, allow_blank=True)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.country = validated_data.get('country', instance.country)
        instance.profile = validated_data.get('profile', instance.profile)
        instance.save()
        return instance


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfiles
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):

        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)

        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')

        url_profile = "https://avatar.oxro.io/avatar.svg?name=" + \
            first_name+"+"+last_name+"&background=ffd60a&color=fff&length=2"
        user.profile = url_profile
        user.save()
        assign_role(user, 'user')

        return user

    def validate(self, attrs):
        password = attrs.get('password', None)
        if password is None:
            raise serializers.ValidationError("Password is required.")
        errors = dict()
        try:
            password_validation.validate_password(password)
        except exceptions.ValidationError as e:

            errors['password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)

        return super(RegisterUserSerializer, self).validate(attrs)


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        update_last_login(None, user)
        return token

    def validate(self, attrs):
        user = UserProfiles.objects.filter(
            email=attrs.get('email', '')).first()
        if user is None:
            raise serializers.ValidationError("User not found.")
        if not user.is_email_verified:
            raise serializers.ValidationError("User is not verified.")

        return super(LoginSerializer, self).validate(attrs)
