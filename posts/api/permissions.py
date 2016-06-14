from django.contrib.auth import get_user
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    message = 'you must be owner of this object.'
    # my_safe_method = ['GET', 'PUT']   # to customize permissions.
    #
    # def has_permission(self, request, view):
    #     if request.method in self.my_safe_method:
    #         return True
    #     return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == get_user(request)