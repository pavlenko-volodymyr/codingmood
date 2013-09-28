from django.contrib import admin

from .models import Commit


class CommitAdmin(admin.ModelAdmin):
    list_display = ('commit_id', 'code_rate', 'date', 'prev_date',)

admin.site.register(Commit, CommitAdmin)
