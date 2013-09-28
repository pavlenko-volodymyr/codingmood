from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'mood')

admin.site.register(Post, PostAdmin)
