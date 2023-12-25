from typing import Any, Dict
from rest_framework import serializers
from .models import *
from rolepermissions.roles import assign_role

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class UserProfilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfiles
        fields = "__all__"
        depth = 1
        extra_kwargs = {
            'password': {'write_only': True}
        }


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
        user.save()
        assign_role(user, 'user')

        return user


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        user = UserProfiles.objects.filter(
            email=attrs.get('email', '')).first()
        if user is None:
            raise serializers.ValidationError("User not found.")
        if not user.is_email_verified:
            raise serializers.ValidationError("User is not verified.")

        return super(LoginSerializer, self).validate(attrs)
