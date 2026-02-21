from datetime import date, timedelta
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Tenant, Contract, RentalApplication
from .serializers import TenantSerializer, ContractSerializer, RentalApplicationSerializer
from apps.users.permissions import IsAdminOrManager
from apps.audit.mixins import AuditMixin
from apps.properties.models import Property


class TenantViewSet(AuditMixin, viewsets.ModelViewSet):
    queryset         = Tenant.objects.select_related("user")
    serializer_class = TenantSerializer
    filter_backends  = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status"]
    search_fields    = ["user__first_name", "user__last_name", "user__email"]
    ordering_fields  = ["created_at"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsAdminOrManager()]


class ContractViewSet(AuditMixin, viewsets.ModelViewSet):
    queryset           = Contract.objects.select_related("tenant__user", "property")
    serializer_class   = ContractSerializer
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields   = ["status", "tenant", "property"]
    search_fields      = ["tenant__user__last_name", "property__name"]
    ordering_fields    = ["start_date", "end_date"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsAdminOrManager()]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.role == "tenant":
            qs = qs.filter(tenant__user=self.request.user)
        return qs


class RentalApplicationViewSet(viewsets.ModelViewSet):
    queryset           = RentalApplication.objects.select_related("user", "property")
    serializer_class   = RentalApplicationSerializer
    filter_backends    = [DjangoFilterBackend]
    filterset_fields   = ["status", "property"]

    def get_permissions(self):
        if self.action in ["list", "retrieve", "create"]:
            return [IsAuthenticated()]
        return [IsAdminOrManager()]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.role == "tenant":
            qs = qs.filter(user=self.request.user)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.instance
        old_status = instance.status
        serializer.save()
        new_status = serializer.instance.status
        if new_status == RentalApplication.Status.APPROVED and old_status != RentalApplication.Status.APPROVED:
            app = serializer.instance
            tenant, _ = Tenant.objects.get_or_create(user=app.user, defaults={"status": "active"})
            if not Contract.objects.filter(tenant=tenant, property=app.property, status=Contract.Status.ACTIVE).exists():
                start = date.today()
                end = start + timedelta(days=365)
                Contract.objects.create(
                    tenant=tenant,
                    property=app.property,
                    start_date=start,
                    end_date=end,
                    monthly_rent=app.property.monthly_rent,
                    status=Contract.Status.ACTIVE,
                )
                app.property.status = Property.Status.RENTED
                app.property.save(update_fields=["status"])
