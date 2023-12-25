from rest_framework import serializers
from .models import UserProfiles
from rolepermissions.roles import assign_role


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
