from rest_framework.views import APIView, status, Request, Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import PublicationSerializer, PublicationValidatedSerializer
from users.models import User
from .models import Publication
from friendships.models import Friendship
from followers.models import Follower
from .permissions import IsPublicationOwner
from django.forms.models import model_to_dict
import ipdb


# Create your views here.
class PublicationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsPublicationOwner]

    def post(self, request: Request) -> Response:
        serializer_validated = PublicationValidatedSerializer(data=request.data)
        serializer_validated.is_valid(raise_exception=True)

        user = False

        try:
            if User.objects.get(username=serializer_validated.data["user_publication"]):
                user = User.objects.get(username=serializer_validated.data["user_publication"]).id
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(email=serializer_validated.data["user_publication"]):
                user = User.objects.get(email=serializer_validated.data["user_publication"]).id
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(id=serializer_validated.data["user_publication"]):
                user = User.objects.get(id=serializer_validated.data["user_publication"]).id
        except (User.DoesNotExist, ValueError):
            if user is False:
                return Response({"message": "User not found"}, status.HTTP_404_NOT_FOUND)

        new_data = {
            "title": serializer_validated.data["title"],
            "text": serializer_validated.data["text"],
            "permission": serializer_validated.data["permission"],
            "photo_url": serializer_validated.data["photo_url"],
            "user_publication": user
        }
        self.check_object_permissions(request, new_data["user_publication"])
        serializer = PublicationSerializer(data=new_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        self.check_object_permissions(request, request.user.id)
        if Publication.objects.filter(user_publication=request.user.id):
            publications = Publication.objects.filter(user_publication=request.user.id)
        else:
            return Response({"message": "Publications is empty"})

        serializer = PublicationSerializer(data=publications, many=True)
        serializer.is_valid()

        return Response(serializer.data, status.HTTP_200_OK)


class PublicationUniqueView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsPublicationOwner]

    def get(self, request: Request, publication_key: str) -> Response:
        self.check_object_permissions(request, request.user.id)
        if publication_key == "public" or publication_key == "private":
            publications = Publication.objects.filter(permission=publication_key, user_publication=request.user.id)
        else:
            if Publication.objects.filter(title=publication_key, user_publication=request.user.id):
                publications = Publication.objects.filter(title=publication_key, user_publication=request.user.id)
            else:
                return Response({"message": 'Publication not found, try passing a title key or permission type "public" or "private"'}, status.HTTP_200_OK)

        serializer = PublicationSerializer(data=publications, many=True)
        serializer.is_valid()

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, publication_key: int) -> Response:
        self.check_object_permissions(request, publication_key)

        try:
            publication = Publication.objects.get(id=publication_key)
            serializer = PublicationSerializer(instance=publication, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status.HTTP_200_OK)
        except (ValueError, Publication.DoesNotExist):
            return Response({"message": "Publication not found"}, status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, publication_key: int) -> Response:
        self.check_object_permissions(request, publication_key)

        try:
            publication = Publication.objects.get(id=publication_key)
            publication.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except (ValueError, Publication.DoesNotExist):
            return Response({"message": "Publication not found"}, status.HTTP_404_NOT_FOUND)


class PublicationsFreeView(APIView):
    def get(self, request: Request) -> Response:
        publications_public = Publication.objects.filter(permission="public")
        serializer_public = PublicationSerializer(data=publications_public, many=True)
        serializer_public.is_valid()

        return Response(serializer_public.data, status.HTTP_200_OK)


class PublicationsPrivateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsPublicationOwner]

    def get(self, request: Request) -> Response:
        self.check_object_permissions(request, request.user.id)

        publications = Publication.objects.filter(permission="private")
        serializer = PublicationSerializer(data=publications, many=True)
        serializer.is_valid()

        publications_allowed = []

        for key in serializer.data:
            if Follower.objects.filter(user_follower=request.user.id, user_following=key["user_publication"]):
                publications_allowed.append(key)

            if Friendship.objects.filter(user_request=request.user.id, user_friendship=key["user_publication"], status="Accepted") or Friendship.objects.filter(user_request=key["user_publication"], user_friendship=request.user.id, status="Accepted"):
                publications_allowed.append(key)

            if key["user_publication"] == request.user.id:
                publications_allowed.append(key)

        serializer = PublicationSerializer(data=publications_allowed, many=True)
        serializer.is_valid()

        return Response(serializer.data, status.HTTP_200_OK)


class TimelineView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsPublicationOwner]

    def get(self, request: Request) -> Response:
        self.check_object_permissions(request, request.user.id)
        pubs_allowed = []
        pubs = Publication.objects.all()

        for key in pubs:
            if key.permission == "private":
                if Follower.objects.filter(user_follower=request.user.id, user_following=key.user_publication):
                    pubs_allowed.insert(0, key)
                if Friendship.objects.filter(user_request=request.user.id, user_friendship=key.user_publication, status="Accepted") or Friendship.objects.filter(user_request=key.user_publication, user_friendship=request.user.id, status="Accepted"):
                    pubs_allowed.insert(0, key)
                if key.user_publication.id == request.user.id:
                    pubs_allowed.insert(0, key)
            else:
                pubs_allowed.insert(0, key)

        serializer = PublicationSerializer(data=pubs_allowed, many=True)
        serializer.is_valid()

        return Response(serializer.data, status.HTTP_200_OK)
