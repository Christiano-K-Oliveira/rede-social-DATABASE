from rest_framework.views import APIView, status, Request, Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LikeValidSerializer, LikeSerializer
from publications.models import Publication
from friendships.models import Friendship
from followers.models import Follower
from .permissions import IsLikeOwner
from .models import Like
import ipdb


# Create your views here.
class LikeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLikeOwner]

    def post(self, request: Request) -> Response:
        self.check_object_permissions(request, request.user.id)
        serializer_validated = LikeValidSerializer(data=request.data)
        serializer_validated.is_valid(raise_exception=True)

        new_data = {
            "user_like": request.user.id,
            "publication": serializer_validated.data["publication"]
        }

        try:
            if Publication.objects.get(id=new_data["publication"]):
                pub = Publication.objects.get(id=new_data["publication"])
                if pub.permission == "private":
                    if Follower.objects.filter(user_follower=request.user.id, user_following=pub.user_publication.id):
                        pass
                    if Friendship.objects.filter(user_request=request.user.id, user_friendship=pub.user_publication.id, status="Accepted") or Friendship.objects.filter(user_request=pub.user_publication.id, user_friendship=request.user.id, status="Accepted"):
                        pass
                    if pub.user_publication.id == request.user.id:
                        pass
                    else:
                        return Response({"message": "User not allowed to like private post without being a friend or follower"})
        except Publication.DoesNotExist:
            return Response({"message": "Publication not found"}, status.HTTP_404_NOT_FOUND)

        serializer = LikeSerializer(data=new_data)
        serializer.is_valid()
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)
    
    def get(self, request: Request) -> Response:
        self.check_object_permissions(request, request.user.id)

        likes = Like.objects.filter(user_like=request.user.id)
        serializer = LikeSerializer(data=likes, many=True)
        serializer.is_valid()

        return Response(serializer.data, status.HTTP_200_OK)


class LikeUniqueView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLikeOwner]

    def get(self, request: Request, publication_key: str) -> Response:
        self.check_object_permissions(request, request.user.id)
        pub = False

        try:
            if Publication.objects.get(id=publication_key):
                pub = Publication.objects.get(id=publication_key).id
                pub_is_my = Publication.objects.get(id=publication_key)

                if pub_is_my.user_publication.id != request.user.id:
                    return Response({"message": "This post does not belong to the past user"}, status.HTTP_400_BAD_REQUEST)
        except (Publication.DoesNotExist, ValueError):
            return Response({"message": "Publication not found"}, status.HTTP_404_NOT_FOUND)

        likes = Like.objects.filter(publication=pub)
        serializer = LikeSerializer(data=likes, many=True)
        serializer.is_valid()

        return Response(serializer.data, status.HTTP_200_OK)
    
    def delete(self, request: Request, publication_key: str) -> Response:
        self.check_object_permissions(request, request.user.id)
        pub = False
        like = False

        try:
            if Publication.objects.get(id=publication_key):
                pub = Publication.objects.get(id=publication_key).id
        except (Publication.DoesNotExist, ValueError):
            return Response({"message": "Publication not found"}, status.HTTP_404_NOT_FOUND)

        try:
            if Like.objects.get(publication=pub, user_like=request.user.id):
                like = Like.objects.get(publication=pub, user_like=request.user.id)
        except (Like.DoesNotExist, ValueError):
            return Response({"message": "Like not found"}, status.HTTP_404_NOT_FOUND)

        like.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)