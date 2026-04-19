from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .permissions import IsStaffOrAdmin, IsOwnerOrAdmin
from services.user_service import (
    create_user,
    authenticate_user,
    generate_tokens,
    get_user_by_id,
    update_user,
    delete_user,
    get_users,
)


# ── Helpers ──────────────────────────────────────────────────────────────────

def success(data=None, message=None, status_code=200, **kwargs):
    body = {'success': True}
    if message:
        body['message'] = message
    if data is not None:
        body['data'] = data
    body.update(kwargs)
    return Response(body, status=status_code)


def error(message, status_code=400, errors=None):
    body = {'success': False, 'error': message}
    if errors:
        body['errors'] = errors
    return Response(body, status=status_code)


# ── Pagination ────────────────────────────────────────────────────────────────

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# ── Register ──────────────────────────────────────────────────────────────────

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return error("Validation xetasi", 400, serializer.errors)

        user = create_user(serializer.validated_data)
        tokens = generate_tokens(user)

        return success(data=UserSerializer(user).data, status_code=201, tokens=tokens)


# ── Login ─────────────────────────────────────────────────────────────────────

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return error("Validation xetasi", 400, serializer.errors)

        user = authenticate_user(
            serializer.validated_data['email'],
            serializer.validated_data['password'],
        )
        if user is None:
            return error("Email ve ya sifre yanlisdir.", status.HTTP_401_UNAUTHORIZED)

        tokens = generate_tokens(user)
        return success(data=UserSerializer(user).data, message="Ugurla giris edildi.", tokens=tokens)


# ── Logout ────────────────────────────────────────────────────────────────────

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return error("Refresh token teleb olunur.", 400)
        try:
            RefreshToken(refresh_token).blacklist()
        except TokenError:
            return error("Token etibarsiz ve ya muddeti bitib.", 400)
        return success(message="Ugurla cixis edildi.")


# ── Me ────────────────────────────────────────────────────────────────────────

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return success(data=UserSerializer(request.user).data)

    def patch(self, request):
        user = update_user(request.user, request.data)
        return success(data=UserSerializer(user).data)


# ── User List + Create ────────────────────────────────────────────────────────

class UserListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrAdmin]
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        filters = {}
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            filters['is_active'] = is_active.lower() in ['true', '1', 'yes']

        role = request.query_params.get('role')
        if role:
            filters['role'] = role

        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering', '-created_at')

        queryset = get_users(filters=filters, search=search, ordering=ordering)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        if page is not None:
            return Response({
                'success': True,
                'data': UserSerializer(page, many=True).data,
                'pagination': {
                    'count': paginator.page.paginator.count,
                    'next': paginator.get_next_link(),
                    'previous': paginator.get_previous_link(),
                    'page_size': paginator.page_size,
                },
            })

        return success(data=UserSerializer(queryset, many=True).data)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return error("Validation xetasi", 400, serializer.errors)
        user = create_user(serializer.validated_data)
        return success(data=UserSerializer(user).data, status_code=201)


# ── User Detail ───────────────────────────────────────────────────────────────

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def _get_user_or_404(self, user_id):
        user = get_user_by_id(user_id)
        if not user:
            return None, error("Istifadeci tapilmadi.", 404)
        return user, None

    def get(self, request, id):
        user, err = self._get_user_or_404(id)
        if err:
            return err
        self.check_object_permissions(request, user)
        return success(data=UserSerializer(user).data)

    def put(self, request, id):
        user, err = self._get_user_or_404(id)
        if err:
            return err
        self.check_object_permissions(request, user)
        return success(data=UserSerializer(update_user(user, request.data)).data)

    def patch(self, request, id):
        user, err = self._get_user_or_404(id)
        if err:
            return err
        self.check_object_permissions(request, user)
        return success(data=UserSerializer(update_user(user, request.data)).data)

    def delete(self, request, id):
        user, err = self._get_user_or_404(id)
        if err:
            return err
        self.check_object_permissions(request, user)
        delete_user(user)
        return success(message="Istifadeci silindi.")