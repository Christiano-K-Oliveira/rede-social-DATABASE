from rest_framework import permissions
from rest_framework.views import View
from .models import Publication
import ipdb


class IsPublicationOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: str) -> bool:
        if request.method == "GET":
            return request.user.is_authenticated
        if request.method == "PATCH" or request.method == "DELETE":
            try:
                if Publication.objects.get(id=int(obj)):
                    pub = Publication.objects.get(id=int(obj))

                    if pub.user_publication.id != request.user.id:
                        return False
                    else:
                        return True
            except (ValueError, Publication.DoesNotExist):
                return True

        return request.user.is_authenticated and request.user.id == int(obj)
