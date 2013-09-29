from django.contrib import admin

from .models import Commit


class CommitAdmin(admin.ModelAdmin):
    list_display = (
        'commit_id', 'code_rate', 'cyclomatic_complexity',
        'cyclomatic_complexity_rank', 'n_of_row_added',
        'n_of_row_deleted', 'date', 'author'
    )

admin.site.register(Commit, CommitAdmin)
