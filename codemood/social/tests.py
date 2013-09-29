import urllib2
import urllib
from StringIO import StringIO
import json
import time
from datetime import datetime

import requests
from social_auth.db.django_models import UserSocialAuth
from mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Post
from .utils import get_text_sentiment_analysis
from .tasks import grab_users_posts


MOCK_ANALYSIS_RESPONSE = {'probability': {'pos': 0.234, 'neg': 0.712, 'neutral': 0.456}, 'label': 'neg'}
MOCK_FACEBOOK_POSTS = [
    {'created_time': 123123,
     'permalink': 'http://example.com',
     'message': 'great text about something important'
    },
    {'created_time': 340340,
     'permalink': 'http://mega-example.com',
     'message': 'boring text about something'
    },
]


def mock_analysis_response(*args, **kwargs):
    class Response(object):
        @staticmethod
        def json():
            return MOCK_ANALYSIS_RESPONSE

    x = Response()
    return Response()


def mock_facebook_auth_response(*args, **kwargs):
    """
    Mock obtaining of facebook access token
    """
    return StringIO('access_token=123&expires=4444')


def mock_facebook_response(*args, **kwargs):
    """
    Mock facebook api response with 2 posts
    """
    return StringIO(json.dumps(MOCK_FACEBOOK_POSTS))


class PostTest(TestCase):
    def test_get_absolute_mood(self):
        post = Post(mood_positive=7, mood_negative=2)

        self.assertEqual(post.get_absolute_mood(), 5)


class TestSentimentAnalysis(TestCase):
    def test_get_text_sentiment_analysis_empty_text(self):
        """
        Say NO to empty strings parsing!
        """
        self.assertRaises(AssertionError, get_text_sentiment_analysis, '')

    def test_get_text_sentiment_analysis(self):
        """
        Tests if
        """
        with patch.object(requests, 'post', new=mock_analysis_response) as mock_method:
            not_realy_random_text = 'not realy random text'
            res = get_text_sentiment_analysis(not_realy_random_text)

            self.assertEqual(res['neg'], 7)
            self.assertEqual(res['pos'], 2)
            self.assertEqual(res['neutral'], 5)
            self.assertEqual(res['total'], 'neg')


class TestFacebookScrapping(TestCase):
    user_facebook_id = 123

    def setUp(self):
        self.extra_data = {'access_token': '100500'}
        self.user = User.objects.create(username='omguser', email='omg@exaple.com')
        self.social_user = UserSocialAuth.objects.create(user=self.user,
                                                         uid=self.user_facebook_id,
                                                         extra_data=self.extra_data)

    def test_grab_users_posts_date_type(self):
        self.assertRaises(AssertionError, grab_users_posts, self.user_facebook_id, 1231)
        self.assertRaises(AssertionError, grab_users_posts, self.user_facebook_id, datetime.now(), 'string')

    def test_grab_users_posts(self):
        with patch.object(urllib, 'urlopen', new=mock_facebook_auth_response) as mock_method:
            with patch.object(urllib2, 'urlopen', new=mock_facebook_response) as mock_method:
                with patch.object(requests, 'post', new=mock_analysis_response) as mock_method:
                    res = grab_users_posts(self.user_facebook_id)
                    self.assertTrue(res)

                    posts = Post.objects.order_by('pk')
                    self.assertEqual(len(posts), 2)

                    post = posts[0]

                    """
                    As we mocked facebook response with mock_posts_response
                    and get_text_sentiment_analysis with MOCK_NEGATIVE_RESPONSE
                    we should have same data saved in model
                    """
                    self.assertEqual(post.content, MOCK_FACEBOOK_POSTS[0]['message'])
                    self.assertEqual(post.link, MOCK_FACEBOOK_POSTS[0]['permalink'])
                    self.assertEqual(int(time.mktime(post.created.timetuple())), MOCK_FACEBOOK_POSTS[0]['created_time'])
                    self.assertEqual(post.link, MOCK_FACEBOOK_POSTS[0]['permalink'])
                    self.assertEqual(post.mood_negative, 7)
                    self.assertEqual(post.mood_positive, 2)
                    self.assertEqual(post.mood_neutral, 5)
                    self.assertEqual(post.mood, 'neg')
