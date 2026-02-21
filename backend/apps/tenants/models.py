from django.db import models
from django.conf import settings
from apps.properties.models import Property


class TenantStatus(models.TextChoices):
    ACTIVE = "active", "Активный"
    INACTIVE = "inactive", "Неактивный"


class Tenant(models.Model):
    user              = models.OneToOneField(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE, related_name="tenant_profile")
    passport_number   = models.CharField(max_length=50, blank=True)
    emergency_contact = models.CharField(max_length=200, blank=True)
    notes             = models.TextField(blank=True)
    status            = models.CharField(max_length=20, choices=TenantStatus.choices, default=TenantStatus.ACTIVE)
    created_at        = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = "Арендатор"
        verbose_name_plural = "Арендаторы"
        ordering = ["-created_at"]

    def __str__(self): return str(self.user)


class RentalApplication(models.Model):
    """Заявка арендатора на аренду свободного объекта."""
    class Status(models.TextChoices):
        PENDING  = "pending",  "На рассмотрении"
        APPROVED = "approved", "Одобрена"
        REJECTED = "rejected", "Отклонена"

    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rental_applications")
    property    = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="rental_applications")
    message          = models.TextField(blank=True)
    desired_start    = models.DateField(null=True, blank=True, verbose_name="Желаемая дата начала")
    desired_end      = models.DateField(null=True, blank=True, verbose_name="Желаемая дата окончания")
    status           = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    rejection_reason = models.TextField(blank=True, verbose_name="Причина отклонения")
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = "Заявка на аренду"
        verbose_name_plural = "Заявки на аренду"
        ordering = ["-created_at"]


class Contract(models.Model):
    class Status(models.TextChoices):
        ACTIVE     = "active",     "Активный"
        EXPIRED    = "expired",    "Истёк"
        TERMINATED = "terminated", "Расторгнут"

    tenant       = models.ForeignKey(Tenant,   on_delete=models.CASCADE, related_name="contracts")
    property     = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="contracts")
    start_date   = models.DateField()
    end_date     = models.DateField()
    monthly_rent = models.DecimalField(max_digits=12, decimal_places=2)
    deposit      = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status       = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    document     = models.FileField(upload_to="contracts/", blank=True, null=True)
    notes        = models.TextField(blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Договор аренды"
        verbose_name_plural = "Договоры аренды"
        ordering = ["-created_at"]

