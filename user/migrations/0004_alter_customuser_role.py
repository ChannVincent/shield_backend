# Generated by Django 5.1.4 on 2025-01-01 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0003_customuser_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="role",
            field=models.CharField(
                choices=[
                    ("ADMIN", "Administrator"),
                    ("MODERATOR", "Moderator"),
                    ("USER LVL 3", "User level 3"),
                    ("USER LVL 2", "User level 2"),
                    ("USER LVL 1", "User level 1"),
                ],
                default="USER LVL 1",
                max_length=20,
            ),
        ),
    ]