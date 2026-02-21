from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"",               views.ServiceRequestViewSet, basename="request")
router.register(r"comments/list",  views.RequestCommentViewSet, basename="comment")
router.register(r"categories/list", views.RequestCategoryViewSet, basename="req-cat")

urlpatterns = [path("", include(router.urls))]


