from rest_framework import serializers
from rest_framework.views import Response
from .models import Like


class LikeValidSerializer(serializers.Serializer):
    publication = serializers.IntegerField()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "created_at", "user_like", "publication"]
        extra_kwargs = {
            "created_at": {"read_only": True},
        }

    def create(self, validated_data: dict) -> Like:
        return Like.objects.create(**validated_data)

    def update(self, instance: Like, validated_data: dict) -> Like:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
