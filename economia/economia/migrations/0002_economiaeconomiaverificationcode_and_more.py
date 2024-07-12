# Generated by Django 4.2.13 on 2024-07-11 09:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("economia", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="EconomiaEconomiaverificationcode",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("email", models.CharField(max_length=254, unique=True)),
                ("code", models.CharField(max_length=6)),
                ("created_at", models.DateTimeField()),
            ],
            options={
                "db_table": "economia_economiaverificationcode",
                "managed": False,
            },
        ),
        migrations.AlterModelOptions(
            name="economiaverificationcode",
            options={"managed": False},
        ),
    ]