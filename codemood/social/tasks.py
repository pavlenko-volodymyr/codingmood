from datetime import datetime
from urlparse import urlparse, parse_qs

from celery import task
from facebook import GraphAPI
from social_auth.db.django_models import UserSocialAuth

from django.conf import settings

from .utils import get_text_sentiment_analysis
from .models import Post


@task
def grab_users_posts(facebook_id):
    user_social_profile = UserSocialAuth.objects.get(uid=facebook_id)

    graph = GraphAPI(user_social_profile.extra_data.get('access_token'))

    graph.extend_access_token(settings.FACEBOOK_APP_ID, settings.FACEBOOK_API_SECRET)

    limit = 100500
    # TODO add limitations by start and end time
    query = 'SELECT created_time, message, permalink FROM stream WHERE source_id = %(user_id)d and message != "" LIMIT %(limit)d' % {'user_id': facebook_id, 'limit': limit}
    res = graph.fql(query)

    for post in res:
        post = Post(user=user_social_profile.user,
                    created=datetime.fromtimestamp(post.get('created_time')),
                    content=post.get('message'),
                    link=post.get('permalink'),
                 )
        mood_stats = get_text_sentiment_analysis(post.content)
        post.mood = mood_stats.get('total')
        post.mood_positive = mood_stats.get('pos')
        post.mood_negative = mood_stats.get('neg')
        post.mood_neutral = mood_stats.get('neutral')

        post.save()
