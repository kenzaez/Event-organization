# Generated by Django 5.2 on 2025-04-30 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("eventApp", "0011_user"),
    ]

    operations = [
        migrations.DeleteModel(
            name="User",
        ),
    ]
