import os

from django.conf import settings
from rest_framework import serializers

from apps.user.models import User


class UserListSerializer(serializers.ModelSerializer):
    # Task 7 üçün list endpoint-də client-ə yalnız təhlükəsiz və lazım olan field-lər qaytarılır.
    class Meta:
        model = User
        fields = (
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


class UserAvatarUploadSerializer(serializers.ModelSerializer):
    # Task 8 üçün avatar upload zamanı yalnız image fayl formatlarına icazə verilir.
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
    allowed_content_types = {'image/jpeg', 'image/png', 'image/webp'}

    class Meta:
        model = User
        fields = ('id', 'avatar')
        read_only_fields = ('id',)

    def validate_avatar(self, value):
        # Maksimum ölçü settings-dən oxunur ki, sonradan ayrıca config ilə rahat dəyişdirilsin.
        max_upload_size = getattr(settings, 'MAX_UPLOAD_IMAGE_SIZE', 2 * 1024 * 1024)
        file_extension = os.path.splitext(value.name)[1].lower()
        content_type = getattr(value, 'content_type', None)

        # Extension yoxlaması istifadəçinin .exe və ya başqa uyğun olmayan fayl göndərməsinin qarşısını alır.
        if file_extension not in self.allowed_extensions:
            raise serializers.ValidationError(
                'Only JPG, JPEG, PNG, and WEBP files are allowed.'
            )

        # Content-Type yoxlaması yalnız uzantıya güvənməmək üçün ayrıca saxlanılır.
        if content_type and content_type not in self.allowed_content_types:
            raise serializers.ValidationError(
                'Unsupported image content type.'
            )

        # Həddən böyük image-lər storage və performans problemi yaratmasın deyə ölçü limiti tətbiq olunur.
        if value.size > max_upload_size:
            raise serializers.ValidationError(
                f'Image size must be {max_upload_size // (1024 * 1024)} MB or less.'
            )

        return value
