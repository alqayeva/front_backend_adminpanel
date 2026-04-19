from django.urls import path

from apps.user.views import UserAvatarUploadAPIView, UserListAPIView


urlpatterns = [
    # Task 7 users list endpoint-i.
    path('', UserListAPIView.as_view(), name='user-list'),
    # Task 8 auth olunmuş user-in öz avatarını yeniləməsi üçün ayrıca route.
    path('me/avatar/', UserAvatarUploadAPIView.as_view(), name='user-avatar-upload'),
]
