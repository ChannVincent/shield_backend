from django.db import models
from django.contrib.auth.models import AbstractUser
from security_data.models import Commune
from cloudinary.models import CloudinaryField
from cloudinary.uploader import destroy


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
    image = CloudinaryField(
        'image', 
        null=True, 
        blank=True, 
        folder='user_image',
        transformation={
            'width': 300,
            'height': 300,
            'crop': 'fill',  # Options: 'fill', 'fit', 'scale', 'thumb', etc.
            'gravity': 'auto',  # Ensures the most important part of the image is retained
        }
    )
    
    # on_save : delete old image
    def save(self, *args, **kwargs):
        if self.pk:
            old_image = CustomUser.objects.filter(pk=self.pk).first().image
            if old_image and str(old_image) != str(self.image):
                destroy(old_image.public_id)
        super().save(*args, **kwargs)
