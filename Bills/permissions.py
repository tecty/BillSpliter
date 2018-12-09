from rest_framework.permissions import BasePermission, AllowAny


class NoCreation(BasePermission):
    message = "Couldn't be created"

    def has_permission(self, request, view):
        if request.method == "POST":
            return False


class IsOwnerOrReadOnly(BasePermission):
    message = 'Only owner can change update this'

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner and \
                request.user.is_authenticated:
            return True
        return False


class UserCreation(BasePermission):
    message = 'You are not the account owner'

    def has_object_permission(self, request, view, obj):
        if request.user.username != obj.username:
            return True
        return False
