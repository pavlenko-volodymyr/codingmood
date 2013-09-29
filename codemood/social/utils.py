import requests


def get_text_sentiment_analysis(text):
    """
    returns dict {pos, neg, neutral, total}
    """
    #no need to analyse empty strings
    assert text

    response = requests.post('http://text-processing.com/api/sentiment/', {'text': text}).json()
    return {'pos': round(response.get('probability').get('pos')*10, 0),
            'neg': round(response.get('probability').get('neg')*10, 0),
            'neutral': round(response.get('probability').get('neutral')*10, 0),
            'total': response.get('label')
    }
