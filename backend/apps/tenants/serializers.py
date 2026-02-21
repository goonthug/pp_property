from rest_framework import serializers
from apps.users.serializers import UserSerializer
from .models import Tenant, Contract, RentalApplication


class TenantSerializer(serializers.ModelSerializer):
    user_detail    = UserSerializer(source="user", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    full_name      = serializers.CharField(source="user.get_full_name", read_only=True)
    email          = serializers.CharField(source="user.email",         read_only=True)
    phone          = serializers.CharField(source="user.phone",         read_only=True)

    class Meta:
        model  = Tenant
        fields = ["id", "user", "user_detail", "full_name", "email", "phone",
                  "passport_number", "emergency_contact", "notes", "status",
                  "status_display", "created_at"]


class RentalApplicationSerializer(serializers.ModelSerializer):
    property_name    = serializers.CharField(source="property.name", read_only=True)
    property_address = serializers.CharField(source="property.address", read_only=True)
    status_display   = serializers.CharField(source="get_status_display", read_only=True)
    user_email       = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model  = RentalApplication
        fields = ["id", "user", "user_email", "property", "property_name", "property_address",
                  "message", "desired_start", "desired_end", "status", "status_display",
                  "rejection_reason", "created_at"]
        read_only_fields = ["user"]

    def validate(self, attrs):
        if self.instance:
            return attrs
        property_obj = attrs.get("property")
        start = attrs.get("desired_start")
        end = attrs.get("desired_end")
        if not start or not end:
            raise serializers.ValidationError(
                {"desired_start": "Укажите желаемый период аренды (дата начала и окончания)."}
            )
        if end <= start:
            raise serializers.ValidationError(
                {"desired_end": "Дата окончания должна быть позже даты начала."}
            )
        overlap = Contract.objects.filter(
            property=property_obj,
            status=Contract.Status.ACTIVE,
        ).filter(start_date__lt=end, end_date__gt=start).exists()
        if overlap:
            raise serializers.ValidationError(
                {"property": "На выбранный период объект уже занят. Выберите другие даты или другой объект."}
            )
        return attrs


class ContractSerializer(serializers.ModelSerializer):
    tenant_name      = serializers.CharField(source="tenant.user.get_full_name", read_only=True)
    property_name    = serializers.CharField(source="property.name",             read_only=True)
    property_address = serializers.CharField(source="property.address",          read_only=True)
    status_display   = serializers.CharField(source="get_status_display",        read_only=True)

    class Meta:
        model  = Contract
        fields = ["id", "tenant", "tenant_name", "property", "property_name",
                  "property_address", "start_date", "end_date", "monthly_rent",
                  "deposit", "status", "status_display", "document", "notes",
                  "created_at", "updated_at"]
