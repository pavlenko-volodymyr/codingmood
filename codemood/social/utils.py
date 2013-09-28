from django.conf import settings
from django.core.cache import cache

from facebook import get_app_access_token
from facebook import GraphAPI


def get_graph_connection():
    token = cache.get('oauth_access_token', False)
    if not token:
        token = get_app_access_token(settings.FACEBOOK_APP_ID, settings.FACEBOOK_API_SECRET)
        cache.set('oauth_access_token', token)

    return GraphAPI(token)

graph_connection = get_graph_connection()