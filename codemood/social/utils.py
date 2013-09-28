import json

from facebook import GraphAPI, get_app_access_token
import requests

from django.conf import settings
from django.core.cache import cache


def get_graph_connection():
    token = cache.get('oauth_access_token', False)
    if not token:
        token = get_app_access_token(settings.FACEBOOK_APP_ID, settings.FACEBOOK_API_SECRET)
        cache.set('oauth_access_token', token)

    return GraphAPI(token)

graph_connection = get_graph_connection()

def get_text_sentiment_analysis(text):
    """
    returns dict {pos, neg, neutral, total}
    """
    #no need to analyse empty strings
    assert text

    response = requests.get('http://text-processing.com/api/sentiment/', {'text': text}).json()

    return {'pos': response.get('probability').get('pos'),
            'neg': response.get('probability').get('neg'),
            'neutral': response.get('probability').get('neutral'),
            'total': response.get('label')
    }
