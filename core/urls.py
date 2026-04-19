from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title='Admin Panel API',
        default_version='v1',
        description=(
            'Next.js admin panel ucun hazirlanan backend API dokumentasiyasi. '
            'Hazirki merhelede users modulu uzre Task 7-9 endpoint-leri dokumentlesdirilib.'
        ),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Users app route-ları ayrıca saxlanılıb ki, app böyüdükcə URL strukturu idarəolunan qalsın.
    path('api/users/', include('apps.user.urls')),
    # Task 11 ucun Swagger / OpenAPI UI burada acilir.
    path('api/docs', schema_view.with_ui('swagger', cache_timeout=0), name='api-docs'),
]

if settings.DEBUG:
    # Development zamanı upload olunan avatar fayllarının birbaşa açılması üçün media route qoşulur.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
