from rest_framework import serializers
from rest_framework.views import Response
from .models import Publication
import ipdb


class PublicationValidatedSerializer(serializers.ModelSerializer):
    user_publication = serializers.CharField()

    class Meta:
        model = Publication
        fields = ["title", "text", "permission", "photo_url", "user_publication", "created_at"]
        extra_kwargs = {
            "created_at": {"read_only": True},
        }


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = ["id", "title", "text", "permission", "photo_url", "user_publication", "created_at"]
        extra_kwargs = {
            "created_at": {"read_only": True},
        }

    def create(self, validated_data: dict) -> Publication:
        return Publication.objects.create(**validated_data)

    def update(self, instance: Publication, validated_data: dict) -> Publication:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
