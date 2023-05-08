from rest_framework import permissions
from followers.models import Follower
from rest_framework.views import View
import ipdb


class IsFollowerOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: Follower) -> bool:
        if request.method == "GET":
            return True

        return request.user.is_authenticated and obj == request.user.id
