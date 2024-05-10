from rest_framework.permissions import BasePermission, SAFE_METHODS
from main import models

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class IsGroupOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class IsGroupAdmins(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return models.GroupUsers.objects.filter(
            group=obj,
            user=request.user,
            is_admin=True
        ).exists()