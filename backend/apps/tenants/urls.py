from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"",               views.TenantViewSet,   basename="tenant")
router.register(r"contracts/list", views.ContractViewSet, basename="contract")

urlpatterns = [path("", include(router.urls))]

