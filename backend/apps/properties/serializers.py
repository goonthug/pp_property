
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
    property_type_name = serializers.CharField(source="property_type.name",  read_only=True)
    status_display     = serializers.CharField(source="get_status_display", read_only=True)
    amenities_detail   = AmenitySerializer(source="amenities", many=True,   read_only=True)

    class Meta:
        model  = Property
        fields = [
            "id", "name", "property_type", "property_type_name",
            "status", "status_display", "address", "area", "floor",
            "rooms", "monthly_rent", "description",
            "amenities", "amenities_detail", "image",
            "created_at", "updated_at",
        ]

