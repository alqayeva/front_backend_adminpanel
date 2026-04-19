from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class EmailBackend(ModelBackend):
    """Email + password ile autentifikasiya."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        email = kwargs.get('email') or username
        if not email or not password:
            return None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None


def create_user(data: dict) -> User:
    return User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        role=data.get('role', 'user'),
    )


def authenticate_user(email: str, password: str):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    if user.check_password(password) and user.is_active:
        return user
    return None


def generate_tokens(user) -> dict:
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def get_users(filters: dict = None, search: str = None, ordering: str = '-created_at'):
    queryset = User.objects.all()

    if filters:
        if 'is_active' in filters:
            queryset = queryset.filter(is_active=filters['is_active'])
        if 'role' in filters:
            queryset = queryset.filter(role=filters['role'])

    if search:
        queryset = queryset.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search)
        )

    return queryset.order_by(ordering)


def get_user_by_id(user_id: int):
    return User.objects.filter(id=user_id).first()


def update_user(user, data: dict) -> User:
    data = dict(data)
    password = data.pop('password', None)
    if password:
        user.set_password(password)
    for key, value in data.items():
        if hasattr(user, key):
            setattr(user, key, value)
    user.save()
    return user


def delete_user(user) -> None:
    user.delete()