from django.db import models
from security_data.models import Commune

class Post(models.Model):
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, null=True, default=None)
    title = models.CharField(max_length=200, null=True, default=None, blank=True)
    text = models.TextField(null=True, default=None, blank=True)
    image = models.ImageField(null=True, default=None, blank=True)
    # video = video upload
    json_data = models.JSONField(null=True, default=None, blank=True)