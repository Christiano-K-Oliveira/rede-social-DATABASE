from rest_framework import permissions
from friendships.models import Friendship
from rest_framework.views import View


class IsFriendshipOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: Follower) -> bool:
        if request.method == "GET":
            return True

        return request.user.is_authenticated and obj == request.user.id
