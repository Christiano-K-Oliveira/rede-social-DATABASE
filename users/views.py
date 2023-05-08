from rest_framework_simplejwt.authentication import JWTAuthentication
from users.models import User
from .permissions import IsAccountOwner
from .serializers import UserSerializer, LoginSerializer, UserReturnSerializer
from rest_framework import generics
from rest_framework.views import APIView, status, Request, Response
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django.forms.models import model_to_dict
import ipdb


# Create your views here.
class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]

    def get(self, request: Request, user_key: str) -> Response:
        user = False

        try:
            if User.objects.get(username=user_key):
                user = User.objects.get(username=user_key)
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(email=user_key):
                user = User.objects.get(email=user_key)
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(id=user_key):
                user = User.objects.get(id=user_key)
        except (User.DoesNotExist, ValueError):
            if user is False:
                return Response({"message: User not found"}, status.HTTP_404_NOT_FOUND)

        serializer = UserReturnSerializer(data=model_to_dict(user))
        serializer.is_valid()

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, user_key: str) -> Response:
        user = False

        try:
            if User.objects.get(username=user_key):
                user = User.objects.get(username=user_key)
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(email=user_key):
                user = User.objects.get(email=user_key)
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(id=user_key):
                user = User.objects.get(id=user_key)
        except (User.DoesNotExist, ValueError):
            if user is False:
                return Response({"message: User not found"}, status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, user)

        serializer = UserSerializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, user_key: str) -> Response:
        user = False

        try:
            if User.objects.get(username=user_key):
                user = User.objects.get(username=user_key)
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(email=user_key):
                user = User.objects.get(email=user_key)
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(id=user_key):
                user = User.objects.get(id=user_key)
        except (User.DoesNotExist, ValueError):
            if user is False:
                return Response({"message: User not found"}, status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, user)

        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginView(APIView):
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_data = serializer.validated_data
        user_find = get_object_or_404(User, email=user_data["email"])
        user_valid = {"username": user_find.username, "password": user_data["password"]}

        user = authenticate(**user_valid)

        if not user:
            return Response({"detail": "No active account found with the given credentials"}, status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        token_dict = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

        return Response(token_dict, status.HTTP_200_OK)
