from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user and request.user.role == 'admin')