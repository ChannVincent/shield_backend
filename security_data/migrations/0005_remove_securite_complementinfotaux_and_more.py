# Generated by Django 5.1.4 on 2024-12-20 23:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("security_data", "0004_securite"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="securite",
            name="complementinfotaux",
        ),
        migrations.RemoveField(
            model_name="securite",
            name="complementinfoval",
        ),
        migrations.RemoveField(
            model_name="securite",
            name="log",
        ),
        migrations.RemoveField(
            model_name="securite",
            name="milllog",
        ),
        migrations.AlterField(
            model_name="securite",
            name="commune",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="security_data.commune",
            ),
        ),
    ]
