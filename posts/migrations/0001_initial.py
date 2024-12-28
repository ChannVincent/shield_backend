# Generated by Django 5.1.4 on 2024-12-28 17:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("security_data", "0005_remove_securite_complementinfotaux_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(default=None, max_length=200, null=True)),
                ("text", models.TextField(default=None, null=True)),
                ("json_data", models.JSONField(default=None, null=True)),
                (
                    "commune",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="security_data.commune",
                    ),
                ),
            ],
        ),
    ]