from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated
from .models import COMMITED, CONCENCUS, FINISH


class NoCreation(BasePermission):
    message = "Couldn't be created"

    def has_permission(self, request, view):
        if request.method == "POST":
            return False

        return True


class IsRelatedOrReadOnly(BasePermission):
    message = 'Only owner can change update this'

    def has_object_permission(self, request, view, obj):
        if (request.method == 'GET' or
            request.user == obj.from_u or
            request.user == obj.to_u) and \
                request.user.is_authenticated:
            return True
        return False


class IsInGroupOrNotPermit(BasePermission):
    message = 'Only user in the group can view the bill'

    def has_object_permission(self, request, view, obj):
        if request.user in obj.group.user_set.all():
            return True
        return False


class IsOwnerOrReadOnly(BasePermission):
    message = 'Only owner can change update this'

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET' or \
            (request.user == obj.owner and
             request.user.is_authenticated):
            return True
        return False


class DelectionProtectedByState(BasePermission):
    """
    Delection can be only perform in lower state than CONCENCUS
    """
    message = 'Only Prepare, Approve, Suspend state can be deleted.'

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE' and \
                obj.state in [COMMITED, CONCENCUS, FINISH]:
            return False
        return True


class UpdateProtectedByState(BasePermission):
    """
    Delection can be only perform in lower state than CONCENCUS
    """
    message = 'Only Prepare, Approve, Suspend state can be deleted.'

    def has_object_permission(self, request, view, obj):
        if request.method in ['POST', "PATCH", "PUT"] and \
                obj.state in [COMMITED, CONCENCUS, FINISH]:
            return False
        return True


class UserCreation(BasePermission):
    message = 'You are not the account owner'

    def has_object_permission(self, request, view, obj):
        if request.user.username != obj.username:
            return True
        return False
