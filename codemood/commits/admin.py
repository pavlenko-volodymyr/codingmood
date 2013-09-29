from django.contrib import admin

from .models import Commit, Repository


class CommitAdmin(admin.ModelAdmin):
    list_display = (
        'commit_id', 'code_rate', 'cyclomatic_complexity',
        'cyclomatic_complexity_rank', 'date', 'author', 'author_email',
    )


class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'url')


admin.site.register(Commit, CommitAdmin)
admin.site.register(Repository, RepositoryAdmin)
