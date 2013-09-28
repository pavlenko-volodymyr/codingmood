from celery import task
from social_auth.db.django_models import UserSocialAuth

from .utils import get_text_sentiment_analysis, graph_connection as graph
from .models import Post

@task
def get_user_timeline(facebook_id):
    user_social_profile = UserSocialAuth.objects.get(uid=facebook_id)
    user = user_social_profile.user

    posts = graph.request(str(facebook_id)+'/feed', args={'fields': 'created_time,message,link,from'})
    for post in posts.get('data', []):
        if not post.get('message', False):
            # no need in posts which we can't analyze
            continue

        post = Post(user=user,
                    created=post.get('created_time'),
                    content=post.get('message'),
                    link=post.get('link'),
                 )
        mood_stats = get_text_sentiment_analysis(post.message)
        post.mood = mood_stats.get('total')
        post.mood_positive = mood_stats.get('pos')
        post.mood_negative = mood_stats.get('neg')
        post.mood_neutral = mood_stats.get('neutral')

        post.save()
