
from rest_framework import serializers
from .models import Payment, PaymentCategory


class PaymentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = PaymentCategory
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display",  read_only=True)
    category_name  = serializers.CharField(source="category.name",       read_only=True)
    tenant_name    = serializers.SerializerMethodField()
    property_name  = serializers.CharField(source="contract.property.name", read_only=True)

    class Meta:
        model  = Payment
        fields = ["id", "contract", "category", "category_name", "amount",
                  "status", "status_display", "due_date", "paid_date",
                  "period_month", "period_year", "receipt", "notes",
                  "tenant_name", "property_name", "created_at", "updated_at"]

    def get_tenant_name(self, obj):
        u = obj.contract.tenant.user
        return u.get_full_name() or u.email

