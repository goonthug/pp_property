from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"categories", views.RequestCategoryViewSet, basename="req-cat")
router.register(r"comments",   views.RequestCommentViewSet, basename="comment")
router.register(r"",          views.ServiceRequestViewSet, basename="request")

urlpatterns = [path("", include(router.urls))]


