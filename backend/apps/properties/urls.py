from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"types",     views.PropertyTypeViewSet, basename="property-type")
router.register(r"amenities", views.AmenityViewSet,    basename="amenity")
router.register(r"",          views.PropertyViewSet,   basename="property")

urlpatterns = [path("", include(router.urls))]

