from rest_framework import serializers
from .models import Friendship
from rest_framework.views import Response
from friendships.models import StatusFields


class FriendshipValidatedSerializer(serializers.ModelSerializer):
    user_request = serializers.CharField()
    user_friendship = serializers.CharField()
    status = serializers.ChoiceField(
        choices=StatusFields.choices
    )

    class Meta:
        model = Friendship
        fields = ["id", "status", "created_at", "user_request", "user_friendship"]
        extra_kwargs = {
            "created_at": {"read_only": True},
        }


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ["id", "status", "created_at", "user_request", "user_friendship"]
        extra_kwargs = {
            "created_at": {"read_only": True},
        }

    def create(self, validated_data: dict) -> Friendship:
        return Friendship.objects.create(**validated_data)

    def update(self, instance: Friendship, validated_data: dict) -> Friendship:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class FriendshipPatchSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=StatusFields.choices
    )
