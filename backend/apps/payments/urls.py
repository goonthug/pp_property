from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"categories", views.PaymentCategoryViewSet, basename="payment-cat")
router.register(r"",           views.PaymentViewSet,         basename="payment")

urlpatterns = [path("", include(router.urls))]

