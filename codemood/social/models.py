from django.db import models
from django.contrib.auth.models import User

MOOD_CHOICES = (
    ('neg', 'Negative'),
    ('pos', 'Positive'),
    ('neutral', 'Neutral'),
)

class Post(models.Model):
    user = models.ForeignKey(User)
    created = models.DateTimeField()
    content = models.TextField()
    mood = models.CharField(choices=MOOD_CHOICES, max_length=15, db_index=True)
    mood_positive = models.SmallIntegerField(default=0)
    mood_negative = models.SmallIntegerField(default=0)
    mood_neutral = models.SmallIntegerField(default=0)
    link = models.URLField()

    def get_absolute_mood(self):
        """
        Calculate mood absolute value from -10 to 10
        """
        return self.mood_positive - self.mood_negative
