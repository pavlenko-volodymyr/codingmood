import time
from datetime import datetime

from celery import task
from facebook import GraphAPI
from social_auth.db.django_models import UserSocialAuth

from django.conf import settings

from .utils import get_text_sentiment_analysis
from .models import Post


@task
def grab_users_posts(facebook_id, start_date=None, end_date=None):
    """
    Grabs users posts from facebook and saves to database

    facebook_id -- users id in facebook
    start_date -- exclude posts created before this date, have to be datetime
    end_date -- exclude posts created after this date, have to be datetime
    """
    if start_date:
        assert type(start_date) is datetime
    if end_date:
        assert type(end_date) is datetime

    user_social_profile = UserSocialAuth.objects.get(uid=facebook_id)

    graph = GraphAPI(user_social_profile.extra_data['access_token'])

    graph.extend_access_token(settings.FACEBOOK_APP_ID, settings.FACEBOOK_API_SECRET)

    # TODO: create real pagination
    limit = 100500

    query = 'SELECT created_time, message, permalink FROM stream ' \
            'WHERE source_id = %(user_id)s and message != ""'

    if start_date:
        query += 'and created_time > %d' % int(time.mktime(start_date.timetuple()))
    if end_date:
        query += 'and created_time < %d' % int(time.mktime(end_date.timetuple()))

    query += ' LIMIT %(limit)d'
    res = graph.fql(query % {'user_id': facebook_id, 'limit': limit})

    for post in res:
        if Post.objects.filter(link=post['permalink']).exists():
            continue

        post = Post(user=user_social_profile.user,
                    created=datetime.fromtimestamp(post['created_time']),
                    content=post['message'],
                    link=post['permalink'],
                    )
        mood_stats = get_text_sentiment_analysis(post.content)
        post.mood = mood_stats['total']
        post.mood_positive = mood_stats['pos']
        post.mood_negative = mood_stats['neg']
        post.mood_neutral = mood_stats['neutral']

        post.save()

    return True
