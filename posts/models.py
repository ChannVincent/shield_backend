from django.db import models
from user.models import CustomUser
from security_data.models import Commune


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, default=None)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, null=True, default=None)
    title = models.CharField(max_length=200, null=True, default=None, blank=True)
    text = models.TextField(null=True, default=None, blank=True)
    type = models.CharField(max_length=50, null=True, default=None, blank=True)
    image = models.ImageField(null=True, default=None, blank=True)
    color = models.CharField(max_length=50, null=True, default=None, blank=True)
    # video = video upload
    json_data = models.JSONField(null=True, default=None, blank=True)