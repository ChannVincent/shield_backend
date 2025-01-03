# Generated by Django 5.1.4 on 2025-01-03 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0005_alter_customuser_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="role",
            field=models.IntegerField(
                choices=[
                    (100, "Admin"),
                    (99, "Developer"),
                    (98, "Moderator"),
                    (9, "User Lvl 9"),
                    (8, "User Lvl 8"),
                    (7, "User Lvl 7"),
                    (6, "User Lvl 6"),
                    (5, "User Lvl 5"),
                    (4, "User Lvl 4"),
                    (3, "User Lvl 3"),
                    (2, "User Lvl 2"),
                    (1, "User Lvl 1"),
                ],
                default=1,
            ),
        ),
    ]
