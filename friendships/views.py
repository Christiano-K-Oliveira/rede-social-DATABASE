from rest_framework.views import APIView, status, Request, Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from .models import Friendship
from users.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import FriendshipValidatedSerializer, FriendshipSerializer
import ipdb


# Create your views here.
class FriendshipView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = []

    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer

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

        if Friendship.objects.filter(user_request=user_request.id, user_friendship=user_friendship.id):
            return Response({"message": "The order already exists"}, status.HTTP_400_BAD_REQUEST)

        new_data = {
            "user_request": user_request.id,
            "user_friendship": user_friendship.id
        }
        serializer = FriendshipSerializer(data=new_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)
