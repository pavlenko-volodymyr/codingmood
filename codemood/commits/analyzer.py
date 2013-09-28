from os.path import join, normpath, isdir
from os import rmdir

from git import Git

from django.conf import settings


def clone_repository(url):
    repo_name = url.split('/')[-1]
    repo_name = repo_name.strip(".git")
    repo_dir_path = normpath(join(settings.GIT_REPOSITORIES_DIR, repo_name))

    if isdir(repo_dir_path):
        rmdir(repo_dir_path)

    Git().clone(url, repo_dir_path)

    return isdir(repo_dir_path)
