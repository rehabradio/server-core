from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user


class IsOwnerOrPlaylistOwnerElseReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners
    of a playlist or the track to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        if obj.owner == request.user or obj.playlist.owner == request.user:
            return True

        return False


class IsStaffToDelete(permissions.BasePermission):
    """
    Object-level permission to only allow admins
    premission to delete a record
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method == 'DELETE':
            return request.user.is_staff

        return True


class IsStaffOrOwnerToDelete(permissions.BasePermission):
    """
    Object-level permission to only allow admins
    premission to delete a record
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method == 'DELETE':
            if obj.owner == request.user or request.user.is_staff:
                return True
            else:
                return False

        return True
