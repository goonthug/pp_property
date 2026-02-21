from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
import django_filters

from .models import Payment, PaymentCategory
from .serializers import PaymentSerializer, PaymentCategorySerializer
from apps.users.permissions import IsAdminOrManager
from apps.audit.mixins import AuditMixin


class PaymentFilter(django_filters.FilterSet):
    min_amount = django_filters.NumberFilter(field_name="amount",   lookup_expr="gte")
    max_amount = django_filters.NumberFilter(field_name="amount",   lookup_expr="lte")
    due_from   = django_filters.DateFilter(field_name="due_date",   lookup_expr="gte")
    due_to     = django_filters.DateFilter(field_name="due_date",   lookup_expr="lte")

    class Meta:
        model  = Payment
        fields = ["status", "category", "contract", "period_year", "period_month"]


class PaymentViewSet(AuditMixin, viewsets.ModelViewSet):
    queryset = Payment.objects.select_related(
        "contract__tenant__user", "contract__property", "category")
    serializer_class = PaymentSerializer
    filter_backends  = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class  = PaymentFilter
    search_fields    = ["contract__tenant__user__last_name", "contract__property__name"]
    ordering_fields  = ["due_date", "amount", "created_at"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsAdminOrManager()]

    def get_queryset(self):
        qs   = super().get_queryset()
        user = self.request.user
        if user.role == "tenant":
            qs = qs.filter(contract__tenant__user=user)
        return qs

    @action(detail=True, methods=["post"])
    def mark_paid(self, request, pk=None):
        """Арендатор отмечает платёж как оплаченный (формальное подтверждение)."""
        payment = self.get_object()
        if request.user.role != "tenant":
            return Response({"detail": "Метод только для арендатора."}, status=403)
        if payment.status == "paid":
            return Response({"detail": "Платёж уже проведён."}, status=400)
        payment.status = "paid"
        payment.paid_date = timezone.now().date()
        payment.save()
        return Response(PaymentSerializer(payment).data)

    def get_permissions(self):
        if self.action in ["list", "retrieve", "mark_paid"]:
            return [IsAuthenticated()]
        return [IsAdminOrManager()]


class PaymentCategoryViewSet(viewsets.ModelViewSet):
    queryset           = PaymentCategory.objects.all()
    serializer_class   = PaymentCategorySerializer
    permission_classes = [IsAdminOrManager]

