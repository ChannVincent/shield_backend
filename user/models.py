from django.db import models
from django.contrib.auth.models import AbstractUser
from security_data.models import Commune


class CustomUser(AbstractUser):
    class Roles(models.IntegerChoices):
        ADMIN = 100
        DEVELOPER = 99
        MODERATOR = 98
        USER_LVL_9 = 9
        USER_LVL_8 = 8
        USER_LVL_7 = 7
        USER_LVL_6 = 6
        USER_LVL_5 = 5
        USER_LVL_4 = 4
        USER_LVL_3 = 3
        USER_LVL_2 = 2
        USER_LVL_1 = 1
        
    phone_number = models.CharField(max_length=15, blank=True, null=True, default=None)
    address = models.CharField(max_length=200, blank=True, null=True, default=None)
    commune = models.ForeignKey(Commune, on_delete=models.DO_NOTHING, null=True, default=None)
    role = models.IntegerField(
        choices=Roles.choices,
        default=Roles.USER_LVL_1,
    )
    image = models.ImageField(null=True, default=None, blank=True)