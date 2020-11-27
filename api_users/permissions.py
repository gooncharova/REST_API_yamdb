from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        else:
            return False


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return False


class IsProfileOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id
