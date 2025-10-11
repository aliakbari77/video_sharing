from rest_framework.permissions import BasePermission

class CanWatchVideo(BasePermission):
    def has_permission(self, request, view):
        # TODO: check if user has active subscription or not
        return super().has_permission(request, view)