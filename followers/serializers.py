from rest_framework import serializers
from .models import Follower
from users.models import User
from rest_framework.views import Response
import ipdb


class FollowerSerializer(serializers.Serializer):
    created_at = serializers.DateTimeField(read_only=True)
    user_follower = serializers.CharField()
    user_following = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.CharField()

    class Meta:
        model = User
        fields = ["id", "name", "username", "email", "password", "birthdate", "bio"]
        extra_kwargs = {
            "password": {"write_only": True},
        }


class UserFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ["created_at", "user_follower", "user_following"]
        extra_kwargs = {
            "created_at": {"read_only": True}
        }

    def create(self, validated_data: dict) -> Follower:
        return Follower.objects.create(**validated_data)
