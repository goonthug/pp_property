from django.db import models
from django.conf import settings


class AuditLog(models.Model):
    class Action(models.TextChoices):
        CREATE = "create", "Создание"
        UPDATE = "update", "Изменение"
        DELETE = "delete", "Удаление"
        LOGIN  = "login",  "Вход"
        LOGOUT = "logout", "Выход"

    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                      null=True, blank=True, related_name="audit_logs")
    action      = models.CharField(max_length=20, choices=Action.choices)
    model_name  = models.CharField(max_length=100, blank=True)
    object_id   = models.PositiveIntegerField(null=True, blank=True)
    object_repr = models.CharField(max_length=500, blank=True)
    changes     = models.JSONField(default=dict)
    ip_address  = models.GenericIPAddressField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = "Запись аудита"
        verbose_name_plural = "Журнал аудита"
        ordering = ["-created_at"]
