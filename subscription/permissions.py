from rest_framework.permissions import BasePermission
from subscription.models import Subscription

class CanWatchVideo(BasePermission):
    message = 'You do not have any active subscription to watch video.'
    
    def has_permission(self, request, view):
        user = request.user
        if Subscription.objects.filter(user=user, is_active=True).exists():
            return True
        return False