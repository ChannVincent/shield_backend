# Generated by Django 5.1.4 on 2024-12-20 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("security_data", "0002_commune_delete_city"),
    ]

    operations = [
        migrations.AlterField(
            model_name="commune",
            name="arrondissement",
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name="commune",
            name="code_commune",
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name="commune",
            name="department",
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name="commune",
            name="region",
            field=models.CharField(max_length=20),
        ),
    ]
