from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/",            views.DashboardStatsView.as_view()),
    path("payments/",             views.PaymentAnalyticsView.as_view()),
    path("properties/",           views.PropertyAnalyticsView.as_view()),
    path("requests/",             views.RequestAnalyticsView.as_view()),
    path("export/payments/csv/",  views.ExportPaymentsCSVView.as_view()),
    path("export/payments/excel/", views.ExportPaymentsExcelView.as_view()),
]

