from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Object-level permission
    Allow owners of an object to update a record.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsOwnerOrPlaylistOwnerElseReadOnly(permissions.BasePermission):
    """Object-level permission
    Allows playlist or playlist track owners to update a record.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.owner == request.user or obj.playlist.owner == request.user:
            return True

        return False


class IsStaffToDelete(permissions.BasePermission):
    """Object-level permission
    Allow admins premission to remove a record
    """

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return request.user.is_staff

        return True


class IsStaffOrOwnerToDelete(permissions.BasePermission):
    """Object-level permission
    Allow admins or owners, premission to remove a record
    """

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            if obj.owner == request.user or request.user.is_staff:
                return True
            else:
                return False

        return True
