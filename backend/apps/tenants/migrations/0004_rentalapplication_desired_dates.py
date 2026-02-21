# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0003_rentalapplication_rejection_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalapplication',
            name='desired_start',
            field=models.DateField(blank=True, null=True, verbose_name='Желаемая дата начала'),
        ),
        migrations.AddField(
            model_name='rentalapplication',
            name='desired_end',
            field=models.DateField(blank=True, null=True, verbose_name='Желаемая дата окончания'),
        ),
    ]
