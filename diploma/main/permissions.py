from rest_framework.permissions import IsAuthenticated, BasePermission, IsAdminUser, AllowAny
from django.contrib.auth.models import User, AnonymousUser

class MainPermission(BasePermission):
    message = 'You must be the admin.'

    def has_permission(self, request, view):
        if view.action is 'list' or view.action is 'retrieve':
            return True
        return False