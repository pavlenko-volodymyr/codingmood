from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'mood', 'mood_positive', 'mood_negative', 'mood_neutral', 'created')
    list_filter = ('mood', 'created')


admin.site.register(Post, PostAdmin)
