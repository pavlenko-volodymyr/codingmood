import re
import sys
import os
from subprocess import Popen, PIPE, STDOUT
from cStringIO import StringIO
from os.path import join, normpath, isdir
from shutil import rmtree

from git import Git, Repo
from pylint import epylint as lint
from pylint.lint import Run

from django.conf import settings


class Analyzer(object):
    code_rate_pattern = re.compile(r"Your code has been rated at ([-0-9.]+)")

    def _lint(self, file_path):
        #old_stdout, old_stderr = sys.stdout, sys.stderr
        #sys.stdout, sys.stderr = StringIO(), StringIO()
        #
        #full_path = os.path.abspath(file_path)
        #parent_path, child_path = os.path.dirname(full_path), os.path.basename(full_path)
        #
        #while parent_path != "/" and os.path.exists(os.path.join(parent_path, '__init__.py')):
        #    child_path = os.path.join(os.path.basename(parent_path), child_path)
        #    parent_path = os.path.dirname(parent_path)
        #
        #lint_options = [
        #    '--msg-template',
        #    '-r', 'n',
        #    '--disable=C,R,I',
        #    child_path  # should be last
        #]
        #Run(" ".join(lint_options), exit=False)
        lint_stdout, lint_stderr = sys.stdout, sys.stderr
        #sys.stdout, sys.stderr = old_stdout, old_stderr
        pylint_stdout, pylint_stderr = lint.py_run(file_path, script='pylint', return_std=True)
        #p = Popen('pylint', stdout=PIPE, stdin=PIPE, stderr=STDOUT, universal_newlines=True)
        #return p.communicate()[0]
        return pylint_stdout.read()

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
        return reversed([i.id for i in self.repo.log()])

    @property
    def python_files(self):
        skip_rules = lambda j: any([
            not j.endswith(".py"),
            j.endswith("__init__.py")
        ])
        return [i for i in self.repo.git.ls_files().split() if not skip_rules(i)]

    def update_repository(self):
        pass

    def pre_commit_checkout(self):
        pass

    def post_commit_checkout(self):
        lint_results = map(float, map(self.lint_file, self.python_files))
        print('Commit code rate: {}'.format(sum(lint_results)))

    def lint_file(self, file_path):
        full_file_path = normpath(join(self.repo_dir_path, file_path))
        lint_report = self._lint(full_file_path)
        match = self.code_rate_pattern.search(lint_report)
        return match.groups()[0] if match else None

    def iterate_commits(self):
        for commit_id in self.commits_ids:
            print('ID {}'.format(commit_id))
            self.pre_commit_checkout()
            self.repo.git.checkout(commit_id)
            self.post_commit_checkout()
        self.repo.git.checkout('master')
