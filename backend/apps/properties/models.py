from django.db import models


class PropertyType(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self): return self.name


class PropertyStatus(models.TextChoices):
    AVAILABLE   = "available",   "Свободно"
    RENTED      = "rented",      "Арендовано"
    MAINTENANCE = "maintenance", "На обслуживании"
    RESERVED    = "reserved",    "Зарезервировано"


class Amenity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self): return self.name


class Property(models.Model):
    name          = models.CharField(max_length=200)
    property_type = models.ForeignKey(PropertyType, on_delete=models.PROTECT,
                                       related_name="properties")
    status        = models.CharField(max_length=20, choices=PropertyStatus.choices,
                                     default=PropertyStatus.AVAILABLE)
    address       = models.CharField(max_length=500)
    area          = models.DecimalField(max_digits=10, decimal_places=2)
    floor         = models.IntegerField(null=True, blank=True)
    rooms         = models.IntegerField(null=True, blank=True)
    monthly_rent  = models.DecimalField(max_digits=12, decimal_places=2)
    description   = models.TextField(blank=True)
    amenities     = models.ManyToManyField(Amenity, blank=True, related_name="properties")
    image         = models.ImageField(upload_to="properties/", blank=True, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Объект недвижимости"
        verbose_name_plural = "Объекты недвижимости"
        ordering = ["-created_at"]

    def __str__(self): return f"{self.name} ({self.address})"

