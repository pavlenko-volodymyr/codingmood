from django.db import models

from model_utils.models import TimeStampedModel


class Repository(TimeStampedModel):
    url = models.URLField()


class Commit(TimeStampedModel):
    #FIXME: should be 38, but maybe i'm wrong
    commit_id = models.CharField(max_length=100)

    code_rate = models.FloatField()

    date = models.DateTimeField()
    prev_date = models.DateTimeField(null=True, blank=True)

    messages = models.TextField(null=True, blank=True)

    author = models.TextField(null=True, blank=True)
    author_email = models.EmailField(null=True, blank=True)

    def __unicode__(self):
        return self.commit_id
