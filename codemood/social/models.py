from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User

MOOD_CHOICES = (
    ('neg', 'Negative'),
    ('pos', 'Positive'),
    ('neutral', 'Neutral'),
)


class PostManager(models.Manager):
    use_for_related_fields = True
    
    @property
    def avarage_mood(self):
        return self.instance.posts.aggregate(Avg('mood_positive')).get('mood_positive__avg',0)\
               -self.instance.posts.aggregate(Avg('mood_negative')).get('mood_negative__avg',0)


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts')
    created = models.DateTimeField()
    content = models.TextField()
    mood = models.CharField(choices=MOOD_CHOICES, max_length=15, db_index=True)
    mood_positive = models.SmallIntegerField(default=0)
    mood_negative = models.SmallIntegerField(default=0)
    mood_neutral = models.SmallIntegerField(default=0)
    link = models.URLField()

    objects = PostManager()

    def get_absolute_mood(self):
        """
        Calculate mood absolute value from -10 to 10
        """
        return self.mood_positive - self.mood_negative
