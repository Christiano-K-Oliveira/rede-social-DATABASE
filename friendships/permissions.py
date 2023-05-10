from rest_framework import permissions
from rest_framework.views import View
from friendships.models import Friendship
import ipdb


class IsFriendshipOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: str) -> bool:
        if request.method == "GET":
            return request.user.is_authenticated and request.user.id == int(obj)
        if request.method == "POST":
            return request.user.is_authenticated
        if request.method == "PATCH":
            if Friendship.objects.filter(user_request=request.user.id, user_friendship=obj):
                return False
            else:
                return request.user.is_authenticated
        if request.method == "DELETE":
            if Friendship.objects.filter(user_request=obj, user_friendship=request.user.id):
                return False
            else:
                return request.user.is_authenticated

        return request.user.is_authenticated and int(obj) == request.user.id
