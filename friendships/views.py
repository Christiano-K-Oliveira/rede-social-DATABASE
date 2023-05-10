from rest_framework.views import APIView, status, Request, Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from .models import Friendship
from users.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import FriendshipValidatedSerializer, FriendshipSerializer, FriendshipPatchSerializer
from .permissions import IsFriendshipOwner
import ipdb


# Create your views here.
class FriendshipView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFriendshipOwner]

    def post(self, request: Request) -> Response:
        serializer = FriendshipValidatedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_request = False
        user_friendship = False

        try:
            if User.objects.get(username=serializer.data["user_request"]) and User.objects.get(username=serializer.data["user_friendship"]):
                user_request = User.objects.get(username=serializer.data["user_request"])
                user_friendship = User.objects.get(username=serializer.data["user_friendship"])
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(email=serializer.data["user_request"]) and User.objects.get(email=serializer.data["user_friendship"]):
                user_request = User.objects.get(email=serializer.data["user_request"])
                user_friendship = User.objects.get(email=serializer.data["user_friendship"])
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(id=serializer.data["user_request"]) and User.objects.get(id=serializer.data["user_friendship"]):
                user_request = User.objects.get(id=serializer.data["user_request"])
                user_friendship = User.objects.get(id=serializer.data["user_friendship"])
        except (User.DoesNotExist, ValueError):
            if user_request is False and user_friendship is False:
                return Response({"message": "Users not found"}, status.HTTP_404_NOT_FOUND)

        if Friendship.objects.filter(user_request=user_request.id, user_friendship=user_friendship.id) or Friendship.objects.filter(user_request=user_friendship.id, user_friendship=user_request.id):
            return Response({"message": "The order already exists"}, status.HTTP_400_BAD_REQUEST)

        self.check_object_permissions(request, request.user)
        new_data = {
            "user_request": user_request.id,
            "user_friendship": user_friendship.id,
            "status": serializer.data["status"]
        }
        serializer = FriendshipSerializer(data=new_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class FriendshipFriendshipUniqueView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFriendshipOwner]

    def get(self, request: Request, friendship_key: str) -> Response:
        friendship = False

        try:
            if User.objects.get(username=friendship_key):
                friendship = User.objects.get(username=friendship_key).id
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(email=friendship_key):
                friendship = User.objects.get(email=friendship_key).id
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(id=friendship_key):
                friendship = User.objects.get(id=friendship_key).id
        except (User.DoesNotExist, ValueError):
            if friendship is False:
                return Response({"message": "Friendship not found"})

        self.check_object_permissions(request, friendship)

        if Friendship.objects.filter(user_friendship=friendship):
            result = Friendship.objects.filter(user_friendship=friendship)
        else:
            return Response({"message": "Not found friend requests for user"}, status.HTTP_400_BAD_REQUEST)

        serializer = FriendshipSerializer(result, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, friendship_key: str) -> Response:
        friendship = friendship_key
        serializer_data = FriendshipPatchSerializer(data=request.data)
        serializer_data.is_valid(raise_exception=True)

        try:
            if User.objects.get(username=friendship_key):
                friendship = User.objects.get(username=friendship_key).id
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(email=friendship_key):
                friendship = User.objects.get(email=friendship_key).id
        except User.DoesNotExist:
            pass

        try:
            if int(friendship):
                pass
        except ValueError:
            return Response({"message": "Friendship not found"}, status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, friendship)

        if Friendship.objects.filter(user_request=friendship, user_friendship=request.user.id):
            result = Friendship.objects.filter(user_request=friendship, user_friendship=request.user.id).first()

        if result is None:
            return Response({"message": "Friend request not found for user"}, status.HTTP_404_NOT_FOUND)

        serializer = FriendshipSerializer(instance=result, data=serializer_data.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, friendship_key: str) -> Response:
        friendship = friendship_key

        try:
            if User.objects.get(username=friendship_key):
                friendship = User.objects.get(username=friendship_key).id
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(email=friendship_key):
                friendship = User.objects.get(email=friendship_key).id
        except User.DoesNotExist:
            pass

        try:
            if int(friendship):
                pass
        except ValueError:
            return Response({"message": "Friendship not found"}, status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, friendship)

        if Friendship.objects.filter(user_request=request.user.id, user_friendship=friendship):
            result = Friendship.objects.filter(user_request=request.user.id, user_friendship=friendship).first()

        if result is None:
            return Response({"message": "Friend request not found for user"}, status.HTTP_404_NOT_FOUND)

        result.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

        ...


class FriendshipRequestUniqueView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFriendshipOwner]

    def get(self, request: Request, friendship_key: str) -> Response:
        friendship = False

        try:
            if User.objects.get(username=friendship_key):
                friendship = User.objects.get(username=friendship_key).id
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(email=friendship_key):
                friendship = User.objects.get(email=friendship_key).id
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(id=friendship_key):
                friendship = User.objects.get(id=friendship_key).id
        except (User.DoesNotExist, ValueError):
            if friendship is False:
                return Response({"message": "Friendship request not found"})

        self.check_object_permissions(request, friendship)

        if Friendship.objects.filter(user_request=friendship):
            result = Friendship.objects.filter(user_request=friendship)
        else:
            return Response({"message": "Not found friend requests for user"}, status.HTTP_400_BAD_REQUEST)

        serializer = FriendshipSerializer(result, many=True)

        return Response(serializer.data, status.HTTP_200_OK)


class FriendshipRequestKeysView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFriendshipOwner]

    def get(self, request: Request, friendship_request_key: str, friendship_key: str) -> Response:
        friendship_request = friendship_request_key
        friendship = friendship_key

        try:
            if User.objects.get(username=friendship_request_key) and User.objects.get(username=friendship_key):
                friendship_request = User.objects.get(username=friendship_request_key).id
                friendship = User.objects.get(username=friendship_key).id
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(email=friendship_request_key) and User.objects.get(email=friendship_key):
                friendship_request = User.objects.get(email=friendship_request_key).id
                friendship = User.objects.get(email=friendship_key).id
        except User.DoesNotExist:
            pass

        self.check_object_permissions(request, friendship_request)

        if Friendship.objects.filter(user_request=friendship_request, user_friendship=friendship):
            result = Friendship.objects.filter(user_request=friendship_request, user_friendship=friendship)
        else:
            return Response({"message": "Not found friend requests for user"}, status.HTTP_400_BAD_REQUEST)

        serializer = FriendshipSerializer(result, many=True)

        return Response(serializer.data, status.HTTP_200_OK)
