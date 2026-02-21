from rest_framework import serializers
from .models import ServiceRequest, RequestComment, RequestCategory


class RequestCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = RequestCategory
        fields = "__all__"


class RequestCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.get_full_name", read_only=True)

    class Meta:
        model  = RequestComment
        fields = ["id", "request", "author", "author_name", "text", "created_at"]
        read_only_fields = ["author", "created_at"]


class ServiceRequestSerializer(serializers.ModelSerializer):
    status_display    = serializers.CharField(source="get_status_display",   read_only=True)
    priority_display  = serializers.CharField(source="get_priority_display", read_only=True)
    category_name     = serializers.CharField(source="category.name",         read_only=True)
    property_name     = serializers.CharField(source="property.name",         read_only=True)
    created_by_name   = serializers.SerializerMethodField()
    assigned_to_name  = serializers.SerializerMethodField()
    comments          = RequestCommentSerializer(many=True, read_only=True)

    class Meta:
        model  = ServiceRequest
        fields = ["id", "title", "description", "property", "property_name",
                  "category", "category_name", "priority", "priority_display",
                  "status", "status_display", "created_by", "created_by_name",
                  "assigned_to", "assigned_to_name", "attachment",
                  "resolved_at", "comments", "created_at", "updated_at"]
        read_only_fields = ["created_by", "created_at", "updated_at"]

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() or obj.created_by.email

    def get_assigned_to_name(self, obj):
        if obj.assigned_to:
            return obj.assigned_to.get_full_name() or obj.assigned_to.email

