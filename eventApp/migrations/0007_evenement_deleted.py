# Generated by Django 5.2 on 2025-04-29 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("eventApp", "0006_remove_evenement_deleted"),
    ]

    operations = [
        migrations.AddField(
            model_name="evenement",
            name="deleted",
            field=models.BooleanField(default=True),
        ),
    ]
