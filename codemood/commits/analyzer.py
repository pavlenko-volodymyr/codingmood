import re
import sys
from math import pow
import os
from subprocess import Popen, PIPE, STDOUT
from cStringIO import StringIO
from os.path import join, normpath, isdir
from os import mkdir
from shutil import rmtree
from time import mktime
from datetime import datetime

from git import Git, Repo
from pylint import epylint as lint
from pylint.lint import Run

from django.conf import settings


from .models import Commit


class Analyzer(object):
    code_rate_pattern = re.compile(r"Your code has been rated at ([-0-9.]+)")

    def _lint(self, file_path):
        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = StringIO(), StringIO()

        lint_options = [
            '--msg-template',
            '-r', 'n',
            '--disable=C,R,I',
            file_path  # should be last
        ]
        try:
            Run(lint_options, exit=False)
        except AttributeError:
            # sometimes we have lint errors with reading file
            self.errors_files.append(file_path)
            return ''
        lint_stdout, lint_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = old_stdout, old_stderr

        return lint_stdout.getvalue()

    def __init__(self, url):
        self.url = url
        self.repo_name = self.url.split('/')[-1].strip(".git")
        self.repo_dir_path = normpath(join(settings.GIT_REPOSITORIES_DIR, self.repo_name))
        self.repo = None if not isdir(normpath(join(self.repo_dir_path, '.git'))) else Repo(self.repo_dir_path)
        self.errors_files = []
        self.commits = []

    def clone_repository(self):
        if isdir(self.repo_dir_path):
            rmtree(self.repo_dir_path)

        mkdir(self.repo_dir_path)

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
        try:
            ids = [i.id for i in self.repo.log()]
        except AttributeError:
            # we have problem with regexp for commit message parsing in pythongit
            ids = self.repo.git.log("master", "--", pretty="%H").splitlines()
        return reversed(ids)

    @property
    def python_files(self):
        skip_rules = lambda j: any([
            not j.endswith(".py"),
            j.endswith("__init__.py"),
            'settings' in j
        ])
        return [i for i in self.repo.git.ls_files().split() if not skip_rules(i)]

    def update_repository(self):
        pass

    def pre_commit_checkout(self, commit_id, prev_commit_id=None):
        pass

    def post_commit_checkout(self, commit_id, prev_commit_id=None):
        lint_results = map(self.lint_file, self.python_files)
        normalization_koef = pow(10.0, len(lint_results)) / 10.0
        code_rates = filter(None, [i['code_rate'] for i in lint_results])
        code_rates = map(float, code_rates)
        code_rate = sum(code_rates) / normalization_koef

        commit = self.repo.commit(commit_id)
        struct_time = commit.committed_date

        # TODO: will convert in localtime, check this
        date = datetime.fromtimestamp(mktime(struct_time))
        data = {
            'commit_id': commit_id, 'date': date,
            'code_rate': code_rate,
            'messages': "\n".join(i['messages'] for i in lint_results),
            'author': commit.author.name,
            'author_email': commit.author.email
        }
        if prev_commit_id:
            prev_struct_time = self.repo.commit(commit_id).committed_date
            prev_date = datetime.fromtimestamp(mktime(prev_struct_time))
            data['prev_date'] = prev_date

        self.commits.append(data)
        print('{commit_id} {code_rate} {author} {author_email}'.format(**data))

    def lint_file(self, file_path):
        full_file_path = normpath(join(self.repo_dir_path, file_path))
        lint_report = self._lint(full_file_path)
        match = self.code_rate_pattern.search(lint_report)
        report = {
            'code_rate': match.groups()[0] if match else None,
            'messages': lint_report
        }
        return report

    def iterate_commits(self):
        prev_commit_id = None
        for commit_id in self.commits_ids:
            self.pre_commit_checkout(commit_id, prev_commit_id)
            self.repo.git.checkout(commit_id)
            self.post_commit_checkout(commit_id, prev_commit_id)
            prev_commit_id = commit_id
        self.repo.git.checkout('master')
        print(self.errors_files)