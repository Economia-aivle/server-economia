# Generated by Django 4.2.13 on 2024-07-11 10:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("economia", "0002_economiaeconomiaverificationcode_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="EconomiaEconomiaverificationcode",
        ),
        migrations.AlterModelTable(
            name="economiaverificationcode",
            table="economia_verificationcode",
        ),
    ]