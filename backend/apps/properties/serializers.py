
from rest_framework import serializers
from .models import Property, PropertyType, Amenity


class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PropertyType
        fields = "__all__"


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Amenity
        fields = "__all__"


class PropertySerializer(serializers.ModelSerializer):
    property_type_name  = serializers.CharField(source="property_type.name", read_only=True)
    status_display     = serializers.CharField(source="get_status_display", read_only=True)
    rental_status_display = serializers.SerializerMethodField()
    amenities_detail   = AmenitySerializer(source="amenities", many=True, read_only=True)

    class Meta:
        model  = Property
        fields = [
            "id", "name", "property_type", "property_type_name",
            "status", "status_display", "rental_status_display", "address", "area", "floor",
            "rooms", "monthly_rent", "description",
            "amenities", "amenities_detail", "image",
            "created_at", "updated_at",
        ]

    def get_rental_status_display(self, obj):
        request = self.context.get("request")
        if request and getattr(request.user, "role", None) in ("admin", "manager"):
            val = getattr(obj, "has_active_contract", False)
            if val is True or (isinstance(val, int) and val != 0):
                return "Арендовано"
            return "Свободно"
        return "Свободно"

