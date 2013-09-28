from django.db import models

from model_utils.models import TimeStampedModel


class Repository(TimeStampedModel):
    url = models.URLField()


class Commit(TimeStampedModel):
    #FIXME: should be 38, but maybe i'm wrong
    commit_id = models.CharField(max_length=100)

    code_rate = models.FloatField()

    date = models.DateTimeField()
    prev_date = models.DateTimeField()

    def __unicode__(self):
        return self.hash
