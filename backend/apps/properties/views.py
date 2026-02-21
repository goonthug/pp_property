from django.db.models import Exists, OuterRef
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
import django_filters

from .models import Property, PropertyType, Amenity
from .serializers import PropertySerializer, PropertyTypeSerializer, AmenitySerializer
from apps.users.permissions import IsAdminOrManager
from apps.audit.mixins import AuditMixin
from apps.tenants.models import Contract


class PropertyFilter(django_filters.FilterSet):
    min_rent = django_filters.NumberFilter(field_name="monthly_rent", lookup_expr="gte")
    max_rent = django_filters.NumberFilter(field_name="monthly_rent", lookup_expr="lte")
    min_area = django_filters.NumberFilter(field_name="area",         lookup_expr="gte")
    max_area = django_filters.NumberFilter(field_name="area",         lookup_expr="lte")

    class Meta:
        model  = Property
        fields = ["status", "property_type", "floor", "rooms"]


class PropertyViewSet(AuditMixin, viewsets.ModelViewSet):
    queryset = Property.objects.select_related("property_type").prefetch_related("amenities")
    serializer_class = PropertySerializer
    filter_backends  = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class  = PropertyFilter
    search_fields    = ["name", "address", "description"]
    ordering_fields  = ["monthly_rent", "area", "created_at"]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.role in ("admin", "manager") and self.action in ("list", "retrieve"):
            today = timezone.now().date()
            active_contract = Contract.objects.filter(
                property=OuterRef("pk"),
                status=Contract.Status.ACTIVE,
                start_date__lte=today,
                end_date__gte=today,
            )
            qs = qs.annotate(has_active_contract=Exists(active_contract))
        return qs

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsAdminOrManager()]


class PropertyTypeViewSet(viewsets.ModelViewSet):
    queryset           = PropertyType.objects.all()
    serializer_class   = PropertyTypeSerializer
    permission_classes = [IsAdminOrManager]


class AmenityViewSet(viewsets.ModelViewSet):
    queryset           = Amenity.objects.all()
    serializer_class   = AmenitySerializer
    permission_classes = [IsAdminOrManager]

