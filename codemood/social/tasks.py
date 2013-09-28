from celery import task

from .utils import graph_connection as graph


@task
def get_user_timeline(facebook_id):
    posts = graph.get_connections(str(facebook_id), 'feed')
