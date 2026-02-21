from django.db import models
from django.conf import settings
from apps.properties.models import Property


class RequestCategory(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self): return self.name


class ServiceRequest(models.Model):
    PRIORITY = [("low","Низкий"),("medium","Средний"),
                ("high","Высокий"),("urgent","Срочный")]
    STATUS   = [("new","Новая"),("in_progress","В работе"),("waiting","Ожидание"),
                ("resolved","Решена"),("closed","Закрыта"),("cancelled","Отменена")]

    title       = models.CharField(max_length=300)
    description = models.TextField()
    property    = models.ForeignKey(Property, on_delete=models.CASCADE,
                                    related_name="service_requests")
    category    = models.ForeignKey(RequestCategory, on_delete=models.PROTECT)
    priority    = models.CharField(max_length=20, choices=PRIORITY, default="medium")
    status      = models.CharField(max_length=20, choices=STATUS,   default="new")
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name="created_requests")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                    null=True, blank=True, related_name="assigned_requests")
    attachment  = models.FileField(upload_to="requests/", blank=True, null=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Заявка на обслуживание"
        verbose_name_plural = "Заявки на обслуживание"
        ordering = ["-created_at"]


class RequestComment(models.Model):
    request    = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE,
                                   related_name="comments")
    author     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text       = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

