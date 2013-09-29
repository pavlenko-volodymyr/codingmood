from django.contrib import admin

from .models import Commit


class CommitAdmin(admin.ModelAdmin):
    list_display = (
        'commit_id', 'code_rate', 'cyclomatic_complexity',
        'cyclomatic_complexity_rank', 'date', 'author', 'author_email',
    )

admin.site.register(Commit, CommitAdmin)
