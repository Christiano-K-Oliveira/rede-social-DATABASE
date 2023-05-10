from rest_framework import permissions
from rest_framework.views import View
from .models import Like


class IsLikeOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: str) -> bool:
        return request.user.is_authenticated
