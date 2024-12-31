from django.contrib import admin

from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('type', 'commune', 'user',)


admin.site.register(Post, PostAdmin)
