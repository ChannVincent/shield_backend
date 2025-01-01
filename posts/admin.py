from django.contrib import admin

from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('type', 'commune', 'user',)


class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
