from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from apps.user.permissions import IsStaffOrAdmin


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


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# ── Products ──────────────────────────────────────────────────────────────────

class ProductListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination

    def get(self, request):
        queryset = Product.objects.select_related('category').all()

        # Search
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        # Filter: category
        category_id = request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Filter: is_active
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() in ['true', '1', 'yes'])

        # Filter: stokda var
        in_stock = request.query_params.get('in_stock')
        if in_stock and in_stock.lower() in ['true', '1']:
            queryset = queryset.filter(stock__gt=0)

        # Ordering
        ordering = request.query_params.get('ordering', '-created_at')
        queryset = queryset.order_by(ordering)

        # Pagination
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        if page is not None:
            return Response({
                'success': True,
                'data': ProductSerializer(page, many=True).data,
                'pagination': {
                    'count': paginator.page.paginator.count,
                    'next': paginator.get_next_link(),
                    'previous': paginator.get_previous_link(),
                    'page_size': paginator.page_size,
                },
            })

        return success(data=ProductSerializer(queryset, many=True).data)

    def post(self, request):
        # Yalnız admin/staff yarat bilər
        if not request.user.role in ['admin', 'staff']:
            return error("İcazəniz yoxdur.", 403)

        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid():
            return error("Validation xətası", 400, serializer.errors)

        product = serializer.save()
        return success(data=ProductSerializer(product).data, status_code=201)


class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_product(self, id):
        product = Product.objects.filter(id=id).select_related('category').first()
        if not product:
            return None, error("Məhsul tapılmadı.", 404)
        return product, None

    def get(self, request, id):
        product, err = self._get_product(id)
        if err:
            return err
        return success(data=ProductSerializer(product).data)

    def put(self, request, id):
        if not request.user.role in ['admin', 'staff']:
            return error("İcazəniz yoxdur.", 403)

        product, err = self._get_product(id)
        if err:
            return err

        serializer = ProductSerializer(product, data=request.data)
        if not serializer.is_valid():
            return error("Validation xətası", 400, serializer.errors)

        product = serializer.save()
        return success(data=ProductSerializer(product).data)

    def patch(self, request, id):
        if not request.user.role in ['admin', 'staff']:
            return error("İcazəniz yoxdur.", 403)

        product, err = self._get_product(id)
        if err:
            return err

        serializer = ProductSerializer(product, data=request.data, partial=True)
        if not serializer.is_valid():
            return error("Validation xətası", 400, serializer.errors)

        product = serializer.save()
        return success(data=ProductSerializer(product).data)

    def delete(self, request, id):
        if not request.user.role in ['admin', 'staff']:
            return error("İcazəniz yoxdur.", 403)

        product, err = self._get_product(id)
        if err:
            return err

        product.delete()
        return success(message="Məhsul silindi.")


# ── Categories ────────────────────────────────────────────────────────────────

class CategoryListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all().order_by('name')
        return success(data=CategorySerializer(categories, many=True).data)

    def post(self, request):
        if not request.user.role in ['admin', 'staff']:
            return error("İcazəniz yoxdur.", 403)

        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            return error("Validation xətası", 400, serializer.errors)

        category = serializer.save()
        return success(data=CategorySerializer(category).data, status_code=201)


class CategoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        if not request.user.role in ['admin', 'staff']:
            return error("İcazəniz yoxdur.", 403)

        category = Category.objects.filter(id=id).first()
        if not category:
            return error("Kateqoriya tapılmadı.", 404)

        category.delete()
        return success(message="Kateqoriya silindi.")