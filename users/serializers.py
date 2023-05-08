from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "username", "email", "password", "birthdate", "bio"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            if key == 'password':
                instance.set_password(value)
            else:
                setattr(instance, key, value)

        instance.save()

        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)


class UserReturnSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.CharField()

    class Meta:
        model = User
        fields = ["id", "name", "username", "email", "password", "birthdate", "bio"]
        extra_kwargs = {
            "password": {"write_only": True},
        }
