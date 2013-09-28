from celery import task


from .analyzer import Analyzer


@task
def process_repository(url):
    repository_analyzer = Analyzer(url)
    repository_analyzer.clone_repository()
    repository_analyzer.iterate_commits()
