# Generated by Django 5.2 on 2025-04-29 13:19

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("eventApp", "0003_client_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="paiement",
            name="deadline",
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
