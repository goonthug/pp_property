from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from .models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"]     = user.email
        token["role"]      = user.role
        token["full_name"] = user.get_full_name()
        return token

    def validate(self, attrs):
        from rest_framework.exceptions import ValidationError
        from .models import User as UserModel
        email = attrs.get("email")
        if email:
            user = UserModel.objects.filter(email=email).first()
            if user and not user.is_active:
                reason = (getattr(user, "block_reason", None) or "").strip() or "Аккаунт заблокирован администратором."
                raise ValidationError({"detail": reason, "block_reason": reason})
        return super().validate(attrs)


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model  = User
        fields = ["id", "email", "username", "first_name", "last_name",
                  "full_name", "role", "phone", "avatar", "is_active",
                  "block_reason", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.email


def validate_phone_value(value):
    if not value or not value.strip():
        return ""
    digits = "".join(c for c in value if c.isdigit())
    if not digits:
        raise serializers.ValidationError("Телефон: только цифры и формат +7.")
    if digits[0] == "8":
        digits = "7" + digits[1:]
    if len(digits) > 11:
        digits = digits[:11]
    if len(digits) != 11 or digits[0] != "7":
        raise serializers.ValidationError("Телефон: +7 и 10 цифр (например +7 999 123-45-67).")
    return "+7" + digits[1:]


class UserCreateSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model  = User
        fields = ["email", "username", "first_name", "last_name",
                  "password", "password2", "role", "phone"]

    def validate_phone(self, value):
        return validate_phone_value(value)

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("password2"):
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        if user.role == "tenant":
            from apps.tenants.models import Tenant
            Tenant.objects.get_or_create(user=user, defaults={"status": "active"})
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Неверный текущий пароль.")
        return value


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ["first_name", "last_name", "phone", "avatar"]

    def validate_phone(self, value):
        return validate_phone_value(value)

