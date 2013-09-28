from urlparse import urlparse, parse_qs

from celery import task
from social_auth.db.django_models import UserSocialAuth

from .utils import get_text_sentiment_analysis, graph_connection as graph
from .models import Post


@task
def get_user_timeline(facebook_id):
    user_social_profile = UserSocialAuth.objects.get(uid=facebook_id)
    user = user_social_profile.user
    limit = 100
    page = graph.request(str(facebook_id)+'/feed', args={'fields': 'created_time,message,link,from', 'limit':limit})
    parse_page(page.get('data', []), user)
    while True:
        if page.get('paging') and page.get('paging').get('next'):
            next_url = urlparse(page.get('paging').get('next'))
            query = parse_qs(next_url.query)

            page = graph.request(str(facebook_id)+'/feed', args={'fields': 'created_time,message,link,from', 'limit':limit, 'until': ','.join(query.get('until'))})
            parse_page(page.get('data', []), user)

            print 'page %s'% ','.join(query.get('until'))
        else:
            return 1

def parse_page(posts, user):
    for post in posts:
        if not post.get('message', False):
            # no need in posts which we can't analyze
            continue

        post = Post(user=user,
                    created=post.get('created_time'),
                    content=post.get('message'),
                    link=post.get('link'),
                 )
        mood_stats = get_text_sentiment_analysis(post.content)
        post.mood = mood_stats.get('total')
        post.mood_positive = mood_stats.get('pos')
        post.mood_negative = mood_stats.get('neg')
        post.mood_neutral = mood_stats.get('neutral')

        post.save()
