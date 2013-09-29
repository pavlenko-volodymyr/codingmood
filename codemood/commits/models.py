from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

from model_utils.models import TimeStampedModel


class CommitManager(models.Manager):
    use_for_related_fields = True

    @property
    def avarage_code_quality(self):
        return self.instance.commits.aggregate(Avg('code_rate'))['code_rate__avg'] or 0


class Repository(TimeStampedModel):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    url = models.URLField()
    last_commit_id = models.CharField(max_length=100, null=True, blank=True)


    @property
    def avarage_code_quality(self):
        return self.id

    def save(self, *args, **kwargs):
        super(Repository, self).save(*args, **kwargs)
        from .tasks import process_repository
        process_repository.delay(self.url, self.id)


class Commit(TimeStampedModel):
    repository = models.ForeignKey(Repository, related_name='commits')
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

    n_of_row_added = models.PositiveIntegerField(default=0)
    n_of_row_deleted = models.PositiveIntegerField(default=0)

    repository = models.ForeignKey(Repository, related_name='commits')

    objects = CommitManager()

    def __unicode__(self):
        return self.commit_id
