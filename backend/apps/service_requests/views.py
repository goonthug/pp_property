from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone

from .models import ServiceRequest, RequestComment, RequestCategory
from .serializers import ServiceRequestSerializer, RequestCommentSerializer, RequestCategorySerializer
from apps.users.permissions import IsAdminOrManager
from apps.audit.mixins import AuditMixin


class ServiceRequestViewSet(AuditMixin, viewsets.ModelViewSet):
    queryset = ServiceRequest.objects.select_related(
        "property", "category", "created_by", "assigned_to"
    ).prefetch_related("comments__author")
    serializer_class = ServiceRequestSerializer
    filter_backends  = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "priority", "category", "property"]
    search_fields    = ["title", "description", "property__name"]
    ordering_fields  = ["created_at", "priority", "status"]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        qs   = super().get_queryset()
        user = self.request.user
        if user.role == "tenant":
            qs = qs.filter(created_by=user)
        return qs

    @action(detail=True, methods=["post"], permission_classes=[IsAdminOrManager])
    def assign(self, request, pk=None):
        req = self.get_object()
        req.assigned_to_id = request.data.get("user_id")
        req.status = "in_progress"
        req.save()
        return Response(ServiceRequestSerializer(req).data)

    @action(detail=True, methods=["post"], permission_classes=[IsAdminOrManager])
    def resolve(self, request, pk=None):
        req = self.get_object()
        req.status = "resolved"
        req.resolved_at = timezone.now()
        req.save()
        return Response(ServiceRequestSerializer(req).data)


class RequestCommentViewSet(viewsets.ModelViewSet):
    queryset           = RequestComment.objects.select_related("author")
    serializer_class   = RequestCommentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend]
    filterset_fields   = ["request"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RequestCategoryViewSet(viewsets.ModelViewSet):
    queryset           = RequestCategory.objects.all()
    serializer_class   = RequestCategorySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsAdminOrManager()]

