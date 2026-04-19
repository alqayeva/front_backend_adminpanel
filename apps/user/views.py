from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, parsers
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.user.models import User
from apps.user.serializers import UserAvatarUploadSerializer, UserListSerializer
from utils.response import success_response


class UserListAPIView(generics.ListAPIView):
    # Task 7-de yalniz users list endpoint-i acilib.
    # Burada CRUD genislendirilmeyib ki, bashqa developerin Task 1-6 ishi ile conflict yaranmasin.
    serializer_class = UserListSerializer
    # Task 10 ucun list endpoint-de yalniz serializerin istifade etdiyi field-ler secilir.
    # Belelikle lazimsiz auth field-leri database-den dasinmir.
    list_response_fields = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'is_active',
        'avatar',
        'created_at',
    )
    # Filter backend-ler view seviyyesinde explicit verilib ki, gelecek merge zamani davranish aydin qalsin.
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    # Frontend active ve inactive user-leri ayird ede bilsin deye boolean filter saxlanilib.
    filterset_fields = ('is_active',)
    # Search yalniz task-da teleb olunan field-ler uzerinden isleyir.
    search_fields = ('username', 'email')
    # Ordering whitelist edilib ki, istenilen field uzerinden siralama aciq qalmasin.
    ordering_fields = ('created_at', 'username', 'email')
    # Default siralama en yeni user-leri evvel gostermek ucundur.
    ordering = ('-created_at',)

    def get_queryset(self):
        # Bu endpoint-de relation olmadigi ucun select_related/prefetch_related fayda vermir.
        # Task 1-6 tamamlandiqdan sonra relation-li model gelerse bu hisse yeniden baxilmalidir.
        return User.objects.only(*self.list_response_fields).order_by('-created_at')

    @swagger_auto_schema(
        operation_summary='Users listesi',
        operation_description=(
            'Task 7 ve Task 9 ucun hazirlanan users list endpoint-i. '
            'Search, filter, ordering ve pagination destekleyir.'
        ),
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description='Username ve email uzre axtarish edir.',
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'is_active',
                openapi.IN_QUERY,
                description='Aktiv ve ya deaktiv user filter-i.',
                type=openapi.TYPE_BOOLEAN,
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description='Pagination ucun sehife nomresi.',
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'page_size',
                openapi.IN_QUERY,
                description='Bir sehifede nece netice olacagini teyin edir.',
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description='created_at, username ve email uzre siralama.',
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserAvatarUploadAPIView(generics.UpdateAPIView):
    # Task 8 ucun ayrica avatar upload endpoint-i secildi.
    # Belelikle umumi user update endpoint-i yazmadan yalniz fayl upload problemi hell olunur.
    serializer_class = UserAvatarUploadSerializer
    # Multipart parser olmadan DRF file upload request-lerini duzgun emal etmir.
    parser_classes = (
        parsers.MultiPartParser,
        parsers.FormParser,
    )
    # Endpoint yalniz partial update kimi isleyir, cunki burada birce avatar field-i yenilenir.
    http_method_names = ['patch']

    def get_object(self):
        # User yalniz oz avatarini deyishsin deye obyekt birbasha request.user-dan goturulur.
        return self.request.user

    @swagger_auto_schema(
        operation_summary='Avatar yukle',
        operation_description=(
            'Task 8 ucun auth olunmus user-in oz avatarini yenileyir. '
            'Request multipart/form-data olmalidir ve avatar acari ile file gonderilmelidir.'
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['avatar'],
            properties={
                'avatar': openapi.Schema(
                    type=openapi.TYPE_FILE,
                    description='JPG, JPEG, PNG ve ya WEBP formatinda image fayli.',
                ),
            },
        ),
    )
    def update(self, request, *args, **kwargs):
        # UpdateAPIView default olaraq serializer data-ni birbasa qaytarir.
        # Task 9-a uygun olmaq ucun burada cavab custom success envelope ile verilir.
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return success_response(
            data=serializer.data,
            message='Avatar updated successfully.',
        )
