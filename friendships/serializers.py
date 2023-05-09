from rest_framework import serializers
from .models import Friendship
from rest_framework.views import Response


class FriendshipValidatedSerializer(serializers.ModelSerializer):
    user_request = serializers.CharField()
    user_friendship = serializers.CharField()

    class Meta:
        model = Friendship
        fields = ["id", "created_at", "user_request", "user_friendship"]
        extra_kwargs = {
            "created_at": {"read_only": True},
        }


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ["id", "created_at", "user_request", "user_friendship"]
        extra_kwargs = {
            "created_at": {"read_only": True},
        }

    def create(self, validated_data: dict) -> Friendship:
        return Friendship.objects.create(**validated_data)
