import calendar
from datetime import date, timedelta
from decimal import Decimal
from django.db import transaction
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Tenant, Contract, RentalApplication
from .serializers import TenantSerializer, ContractSerializer, RentalApplicationSerializer
from apps.users.permissions import IsAdminOrManager
from apps.audit.mixins import AuditMixin
from apps.properties.models import Property, PropertyStatus
from apps.payments.models import Payment, PaymentCategory


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

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def perform_update(self, serializer):
        instance = serializer.instance
        old_status = instance.status
        with transaction.atomic():
            serializer.save()
            new_status = serializer.instance.status
            if new_status != RentalApplication.Status.APPROVED or old_status == RentalApplication.Status.APPROVED:
                return
            app = serializer.instance
            start = getattr(app, "desired_start", None) or date.today()
            end = getattr(app, "desired_end", None) or (start + timedelta(days=365))
            if not isinstance(start, date):
                start = date.today()
            if not isinstance(end, date):
                end = start + timedelta(days=365)
            if end <= start:
                end = start + timedelta(days=365)
            tenant, _ = Tenant.objects.get_or_create(user=app.user, defaults={"status": "active"})
            if Contract.objects.filter(tenant=tenant, property=app.property, status=Contract.Status.ACTIVE).exists():
                return
            monthly_rent = app.property.monthly_rent
            if monthly_rent is None:
                monthly_rent = Decimal("0")
            contract = Contract.objects.create(
                tenant=tenant,
                property=app.property,
                start_date=start,
                end_date=end,
                monthly_rent=monthly_rent,
                status=Contract.Status.ACTIVE,
            )
            app.property.status = PropertyStatus.RENTED
            app.property.save(update_fields=["status"])
            cat, _ = PaymentCategory.objects.get_or_create(name="Аренда", defaults={"description": "Арендная плата"})
            cur = start.replace(day=1)
            while cur <= end:
                due = cur if cur >= start else start
                Payment.objects.get_or_create(
                    contract=contract,
                    category=cat,
                    period_month=cur.month,
                    period_year=cur.year,
                    defaults={
                        "amount": monthly_rent,
                        "status": "pending",
                        "due_date": due,
                    },
                )
                _, last_day = calendar.monthrange(cur.year, cur.month)
                next_first = (cur.replace(day=last_day) + timedelta(days=1))
                cur = next_first.replace(day=1)
