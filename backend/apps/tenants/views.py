from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Tenant, Contract
from .serializers import TenantSerializer, ContractSerializer
from apps.users.permissions import IsAdminOrManager
from apps.audit.mixins import AuditMixin


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
