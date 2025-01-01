from django.db import models
from django.contrib.auth.models import AbstractUser
from security_data.models import Commune


class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        MODERATOR = 'MODERATOR', 'Moderator'
        USER_LVL_3 = 'USER LVL 3', 'User level 3'
        USER_LVL_2 = 'USER LVL 2', 'User level 2'
        USER_LVL_1 = 'USER LVL 1', 'User level 1'
        
    phone_number = models.CharField(max_length=15, blank=True, null=True, default=None)
    address = models.CharField(max_length=200, blank=True, null=True, default=None)
    commune = models.ForeignKey(Commune, on_delete=models.DO_NOTHING, null=True, default=None)
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.USER_LVL_1,
    )
    image = models.ImageField(null=True, default=None, blank=True)