from django.db import models

from model_utils.models import TimeStampedModel


class Repository(TimeStampedModel):
    url = models.URLField()
    last_commit_id = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Repository, self).save(*args, **kwargs)
        from .tasks import process_repository
        process_repository.delay(self.url, self.id)


class Commit(TimeStampedModel):
    #FIXME: should be 38, but maybe i'm wrong
    commit_id = models.CharField(max_length=100)

    code_rate = models.FloatField()

    date = models.DateTimeField()
    prev_date = models.DateTimeField(null=True, blank=True)

    messages = models.TextField(null=True, blank=True)

    author = models.CharField(max_length=125, null=True, blank=True)
    author_email = models.EmailField(null=True, blank=True)

    cyclomatic_complexity = models.IntegerField(default=1)
    cyclomatic_complexity_rank = models.CharField(max_length=1, default='A')

    repository = models.ForeignKey(Repository, related_name='commits')

    def __unicode__(self):
        return self.commit_id
