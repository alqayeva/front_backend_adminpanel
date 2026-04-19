from django.utils.functional import SimpleLazyObject
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


def get_user_jwt(request):
    auth = JWTAuthentication()
    try:
        result = auth.authenticate(request)
        if result is not None:
            return result[0]
    except (InvalidToken, TokenError):
        pass
    return None


class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not hasattr(request, '_cached_user') or not request.user.is_authenticated:
            user = get_user_jwt(request)
            if user is not None:
                request.user = SimpleLazyObject(lambda: user)

        response = self.get_response(request)
        return response