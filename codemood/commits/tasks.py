from celery import task


from .analyzer import Analyzer


@task
def process_repository(url, repository_id, user_id):
    repository_analyzer = Analyzer(url, repository_id=repository_id)
    repository_analyzer.clone_repository()
    repository_analyzer.iterate_commits()

    # run task to give bages
    from badges.tasks import give_badges
    give_badges.delay(user_id)
