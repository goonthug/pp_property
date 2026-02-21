from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r"users", views.UserViewSet, basename="user")

urlpatterns = [
    path("login/",           views.CustomTokenObtainPairView.as_view(), name="login"),
    path("refresh/",         TokenRefreshView.as_view(),                name="token_refresh"),
    path("logout/",          views.LogoutView.as_view(),                name="logout"),
    path("register/",        views.RegisterView.as_view(),              name="register"),
    path("profile/",         views.ProfileView.as_view(),               name="profile"),
    path("change-password/", views.ChangePasswordView.as_view(),        name="change_password"),
    path("", include(router.urls)),
]

