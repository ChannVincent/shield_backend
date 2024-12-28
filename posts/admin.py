from django.contrib import admin

from .models import *


class PostAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
