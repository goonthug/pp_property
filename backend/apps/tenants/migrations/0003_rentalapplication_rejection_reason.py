# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0002_rentalapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalapplication',
            name='rejection_reason',
            field=models.TextField(blank=True, verbose_name='Причина отклонения'),
        ),
    ]
