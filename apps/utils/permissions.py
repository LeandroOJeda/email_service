from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging

logger = logging.getLogger()


class IsSuperUser(BasePermission):
    """
    Allows access only to super users.
    """

    def has_permission(self, request, view):
        jwt_authenticator = JWTAuthentication()
        response = jwt_authenticator.authenticate(request)
        if response is not None:
            _user, token = response
            return bool(token.payload["access_level"] == 0)
        else:
            return False


class IsUser(BasePermission):
    """
    Allows access to users.
    """

    def has_permission(self, request, view):
        jwt_authenticator = JWTAuthentication()
        response = jwt_authenticator.authenticate(request)
        if response is not None:
            _user, token = response
            return bool(token.payload["access_level"] == 1)
        else:
            return False


class IsTeacher(BasePermission):
    """
    Allows access only to teacher users.
    """

    def has_permission(self, request, view):
        jwt_authenticator = JWTAuthentication()
        response = jwt_authenticator.authenticate(request)
        if response is not None:
            _user, token = response
            return bool(token.payload["access_level"] == 2)
        else:
            return False


class IsAdministrative(BasePermission):
    """
    Allows access only to administrative users.
    """

    def has_permission(self, request, view):
        jwt_authenticator = JWTAuthentication()
        response = jwt_authenticator.authenticate(request)
        if response is not None:
            _user, token = response
            return bool(token.payload["access_level"] == 3)
        else:
            return False


class IsSelf(IsAuthenticated):
    """
    Allows access only if the request URL pk is from the authenticated user.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.id
    



