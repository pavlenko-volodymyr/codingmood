from celery import task
from facebook import GraphAPI


@task
def get_user_timeline(facebook_id):
    graph = GraphAPI()
