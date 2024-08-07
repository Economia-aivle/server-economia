# Generated by Django 4.2.13 on 2024-07-21 09:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("economia", "0006_alter_childcomments_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="childcomments",
            name="imgfile",
            field=models.ImageField(blank=True, default="", null=True, upload_to=""),
        ),
        migrations.AddField(
            model_name="childcomments",
            name="parent",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="economia.comments",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="childcomments",
            name="player",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
