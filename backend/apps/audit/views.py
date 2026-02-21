from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import AuditLog
from .serializers import AuditLogSerializer
from apps.users.permissions import IsAdmin


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset           = AuditLog.objects.select_related("user")
    serializer_class   = AuditLogSerializer
    permission_classes = [IsAdmin]
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields   = ["action", "model_name", "user"]
    search_fields      = ["object_repr", "model_name", "user__email"]
    ordering_fields    = ["created_at"]

