from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User)
    created = models.DateTimeField()
    content = models.TextField()
    mood = models.SmallIntegerField(default=0)
    link = models.CharField(max_length=255)
