from os.path import join, normpath, isdir
from shutil import rmtree

from git import Git, Repo

from django.conf import settings


class Analyzer(object):
    # TODO: remove DUMMY_GIT_REPOSITORY
    def __init__(self, url=settings.DUMMY_GIT_REPOSITORY):
        self.url = url
        self.repo_name = self.url.split('/')[-1].strip(".git")
        self.repo_dir_path = normpath(join(settings.GIT_REPOSITORIES_DIR, self.repo_name))
        self.repo = None if not normpath(join(self.repo_dir_path, '.git')) else Repo(self.repo_dir_path)

    def clone_repository(self):
        if isdir(self.repo_dir_path):
            rmtree(self.repo_dir_path)

        Git().clone(self.url, self.repo_dir_path)
        cloned_successful = isdir(self.repo_dir_path)

        # TODO: Remove this
        assert cloned_successful

        self.repo = Repo(self.repo_dir_path)
        return cloned_successful

    @property
    def first_commit(self):
        return next(reversed(self.commits_ids), None)

    @property
    def commits_ids(self):
        return [i.id for i in self.repo.log()]

    @property
    def python_files(self):
        return [i for i in self.repo.git.ls_files().split() if i.endswith(".py")]

    def update_repository(self):
        pass

    def pre_commit_checkout(self):
        pass

    def post_commit_checkout(self):
        print(self.python_files)

    def iterate_commits(self):
        for commit_id in self.commits_ids:
            self.pre_commit_checkout()
            self.repo.git.checkout(commit_id)
            self.post_commit_checkout()
