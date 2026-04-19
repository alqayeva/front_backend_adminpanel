from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bu email artiq istifade olunur.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Bu username artiq istifade olunur.")
        return value

    def validate_role(self, value):
        allowed = [r.value for r in User.Role]
        if value not in allowed:
            raise serializers.ValidationError(f"Role '{value}' etibarsizdir. Secimler: {allowed}")
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_active', 'created_at', 'avatar']
        read_only_fields = ['id', 'created_at']