from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """
    Check user is moderator
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwner(permissions.BasePermission):
    """
    Checks user is the owner
    """

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False