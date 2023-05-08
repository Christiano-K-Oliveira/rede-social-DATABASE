from rest_framework import generics
from .models import Follower
from .serializers import FollowerSerializer, UserFollowerSerializer
from rest_framework.views import APIView, status, Request, Response
from users.models import User
from django.forms.models import model_to_dict
import json
from rest_framework_simplejwt.authentication import JWTAuthentication
from followers.permissions import IsFollowerOwner
import ipdb


# Create your views here.
class FollowersView(generics.ListCreateAPIView):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

    def post(self, request: Request) -> Response:
        serializer = FollowerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_follower = False
        user_following = False

        try:
            if User.objects.get(username=serializer.data["user_follower"]) and User.objects.get(username=serializer.data["user_following"]):
                user_follower = User.objects.get(username=serializer.data["user_follower"])
                user_following = User.objects.get(username=serializer.data["user_following"])
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(email=serializer.data["user_follower"]) and User.objects.get(email=serializer.data["user_following"]):
                user_follower = User.objects.get(email=serializer.data["user_follower"])
                user_following = User.objects.get(email=serializer.data["user_following"])
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(id=int(serializer.data["user_follower"])) and User.objects.get(id=int(serializer.data["user_following"])):
                user_follower = User.objects.get(id=int(serializer.data["user_follower"]))
                user_following = User.objects.get(id=int(serializer.data["user_following"]))
        except (User.DoesNotExist, ValueError):
            if user_follower is False or user_following is False:
                return Response({"message": "Users not found"}, status.HTTP_404_NOT_FOUND)

        if Follower.objects.filter(user_follower=user_follower.id, user_following=user_following.id):
            return Response({"message": "Relation already exists"}, status.HTTP_400_BAD_REQUEST)

        new_data = {
            "user_follower": user_follower.id,
            "user_following": user_following.id
        }
        serializer = UserFollowerSerializer(data=new_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_follower=user_follower, user_following=user_following)

        return Response(serializer.data, status.HTTP_201_CREATED)


class FollowerView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFollowerOwner]

    def get(self, request: Request, follower_key: str, following_key: str) -> Response:
        follower = follower_key
        following = following_key

        try:
            if User.objects.get(username=follower_key) and User.objects.get(username=following_key):
                follower = User.objects.get(username=follower_key).id
                following = User.objects.get(username=following_key).id
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(email=follower_key) and User.objects.get(email=following_key):
                follower = User.objects.get(email=follower_key).id
                following = User.objects.get(email=following_key).id
        except User.DoesNotExist:
            pass

        if Follower.objects.filter(user_follower=follower, user_following=following):
            result = Follower.objects.filter(user_follower=follower, user_following=following)
        else:
            return Response({"message": "Users not found"}, status.HTTP_404_NOT_FOUND)

        serializer = UserFollowerSerializer(result, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, follower_key: str, following_key: str) -> Response:
        follower = False
        following = False

        try:
            if User.objects.get(username=follower_key) and User.objects.get(username=following_key):
                follower = User.objects.get(username=follower_key).id
                following = User.objects.get(username=following_key).id
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(email=follower_key) and User.objects.get(email=following_key):
                follower = User.objects.get(email=follower_key).id
                following = User.objects.get(email=following_key).id
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(id=follower_key) and User.objects.get(id=following_key):
                follower = User.objects.get(id=follower_key).id
                following = User.objects.get(id=following_key).id
        except (User.DoesNotExist, ValueError):
            if follower is False or following is False:
                return Response({"message": "Users not found"}, status.HTTP_404_NOT_FOUND)

        users_relation = Follower.objects.filter(user_follower=follower, user_following=following).first()
        self.check_object_permissions(request, follower)

        if users_relation is None:
            return Response({"message": "The relationship between users does not exist"}, status.HTTP_404_NOT_FOUND)

        users_relation.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowerUniqueView(APIView):
    def get(self, request: Request, follower_type: str, follower_key: str) -> Response:
        follower = follower_key

        if follower_type != "follower" and follower_type != "following":
            return Response({"message": ['Allowed types are "follower" and "following"']})

        try:
            if User.objects.get(username=follower_key):
                follower = User.objects.get(username=follower_key).id
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(email=follower_key):
                follower = User.objects.get(email=follower_key).id
        except User.DoesNotExist:
            pass

        if follower_type == "follower":
            if Follower.objects.filter(user_follower=follower):
                result = Follower.objects.filter(user_follower=follower)
            else:
                return Response({"message": "Follower is empty"}, status.HTTP_400_BAD_REQUEST)
        else:
            if Follower.objects.filter(user_following=follower):
                result = Follower.objects.filter(user_following=follower)
            else:
                return Response({"message": "Following is empty"}, status.HTTP_400_BAD_REQUEST)

        serializer = UserFollowerSerializer(result, many=True)

        return Response(serializer.data, status.HTTP_200_OK)
