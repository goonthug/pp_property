# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='block_reason',
            field=models.TextField(blank=True, verbose_name='Причина блокировки'),
        ),
    ]
