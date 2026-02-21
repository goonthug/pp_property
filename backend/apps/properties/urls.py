from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"",              views.PropertyViewSet,     basename="property")
router.register(r"types/list",   views.PropertyTypeViewSet, basename="property-type")
router.register(r"amenities/list", views.AmenityViewSet,    basename="amenity")

urlpatterns = [path("", include(router.urls))]

