from django.db import models
from user.models import CustomUser
from security_data.models import Commune


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, default=None)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, null=True, default=None)
    title = models.CharField(max_length=200, null=True, default=None, blank=True)
    text = models.TextField(null=True, default=None, blank=True)
    type = models.CharField(max_length=50, null=True, default=None, blank=True)
    image = models.ImageField(upload_to='media/', null=True, default=None, blank=True)
    color = models.CharField(max_length=50, null=True, default=None, blank=True)
    json_data = models.JSONField(null=True, default=None, blank=True)
    likes = models.ManyToManyField(CustomUser, related_name="liked_posts", blank=True)


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"