from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"",               views.PaymentViewSet,         basename="payment")
router.register(r"categories/list", views.PaymentCategoryViewSet, basename="payment-cat")

urlpatterns = [path("", include(router.urls))]

