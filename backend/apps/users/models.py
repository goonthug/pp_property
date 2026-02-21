from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    ADMIN   = "admin",   "Администратор"
    MANAGER = "manager", "Менеджер"
    TENANT  = "tenant",  "Арендатор"


class User(AbstractUser):
    email         = models.EmailField(unique=True)
    role          = models.CharField(max_length=20, choices=Role.choices, default=Role.TENANT)
    phone         = models.CharField(max_length=20, blank=True)
    avatar        = models.ImageField(upload_to="avatars/", blank=True, null=True)
    block_reason  = models.TextField(blank=True, verbose_name="Причина блокировки")
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name        = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_full_name() or self.email} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == Role.ADMIN

    @property
    def is_manager(self):
        return self.role in [Role.ADMIN, Role.MANAGER]

