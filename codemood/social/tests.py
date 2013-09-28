from django.test import TestCase

import requests
from mock import patch

from .models import Post
from .utils import get_text_sentiment_analysis


class PostTest(TestCase):

    def test_get_absolute_mood(self):
        post = Post(mood_positive=7, mood_negative=2)

        self.assertEqual(post.get_absolute_mood(), 5)

class TestSentimentAnalysis(TestCase):
    MOCK_NEGATIVE_RESPONSE= {'probability': {'pos': 0.234, 'neg':0.712, 'neutral': 0.456}, 'label': 'neg'}

    def test_get_text_sentiment_analysis(self):
        def mock_analysis_response(arg, argtwo):
            class Response(object):
                @staticmethod
                def json():
                    return self.MOCK_NEGATIVE_RESPONSE
            x = Response()
            return Response()

        with patch.object(requests, 'post', new=mock_analysis_response) as mock_method:
            not_realy_random_text = """
            get_text_sentiment_analysis
            """
            res = get_text_sentiment_analysis(not_realy_random_text)

            self.assertEqual(res['neg'], 7)
            self.assertEqual(res['pos'], 2)
            self.assertEqual(res['neutral'], 5)
            self.assertEqual(res['total'], 'neg')
