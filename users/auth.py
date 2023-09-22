import jwt
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError
from rest_framework import permissions

User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if jwt_token is None:
            return None
        jwt_token = JWTAuthentication.get_the_token_from_header(jwt_token)

        # Decode the JWT and verify its signature
        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')
        except:
            raise ParseError()
        user_email = payload['user_email']
        user_role = payload['user_role']
        if user_email and user_role is None:
            raise AuthenticationFailed('User  not found in JWT')
        user = User.objects.filter(email=user_email, role=user_role).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        return user, payload

    def authenticate_header(self, request):
        return 'Bearer'

    @classmethod
    def create_payload(cls, user):
        payload = {

            'user_email': user.email,
            'user_role': user.role,
            'exp': int((datetime.now() + timedelta(minutes=settings.JWT_CONF['TOKEN_LIFETIME_MINUTES'])).timestamp()),
            'iat': datetime.now().timestamp(),

        }
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_CONF['JWT_ALGORITHM'])
        return jwt_token

    @classmethod
    def get_the_token_from_header(cls, jwt_token):
        token = jwt_token.replace('Bearer', '').replace(' ', '')
        return token


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user and user.is_authenticated and user.role == 'admin' and user.is_staff is True


# class IsUser(permissions.BasePermission):
#     def has_permission(self, request, view):
#         user = request.user
#         return user and user.is_authenticated and user.role == 'user' and user.is_active is True


class IsProfileOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        else:
            return obj == request.user
