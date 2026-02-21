from django.db import models
from apps.tenants.models import Contract


class PaymentStatus(models.TextChoices):
    PENDING   = "pending",   "Ожидается"
    PAID      = "paid",      "Оплачен"
    OVERDUE   = "overdue",   "Просрочен"
    CANCELLED = "cancelled", "Отменён"


class PaymentCategory(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self): return self.name


class Payment(models.Model):
    contract     = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="payments")
    category     = models.ForeignKey(PaymentCategory, on_delete=models.PROTECT)
    amount       = models.DecimalField(max_digits=12, decimal_places=2)
    status       = models.CharField(max_length=20, choices=PaymentStatus.choices,
                                    default=PaymentStatus.PENDING)
    due_date     = models.DateField()
    paid_date    = models.DateField(null=True, blank=True)
    period_month = models.IntegerField()
    period_year  = models.IntegerField()
    receipt      = models.FileField(upload_to="receipts/", blank=True, null=True)
    notes        = models.TextField(blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Платёж"
        verbose_name_plural = "Платежи"
        ordering = ["-due_date"]

