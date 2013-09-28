from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User)
    created = models.DateTimeField()
    content = models.TextField()
    mood = models.CharField(max_length=15, db_index=True)
    mood_positive = models.SmallIntegerField(default=0)
    mood_negative = models.SmallIntegerField(default=0)
    mood_neutral = models.SmallIntegerField(default=0)
    link = models.CharField(max_length=255)
