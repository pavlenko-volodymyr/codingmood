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

    def __init__(self, url):
        self.url = url
        self.repo_name = self.url.split('/')[-1].strip(".git")
        self.repo_dir_path = normpath(join(settings.GIT_REPOSITORIES_DIR, self.repo_name))
        self.repo = None if not isdir(normpath(join(self.repo_dir_path, '.git'))) else Repo(self.repo_dir_path)

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
        return reversed([i.id for i in self.repo.log()])

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
        code_rate = sum([float(i['code_rate']) for i in lint_results]) / normalization_koef
        struct_time = self.repo.commit(commit_id).committed_date

        # TODO: will convert in localtime, check this
        date = datetime.fromtimestamp(mktime(struct_time))
        data = {
            'commit_id': commit_id, 'date': date,
            'code_rate': code_rate,
            'messages': "\n".join(i['messages'] for i in lint_results)
        }
        if prev_commit_id:
            prev_struct_time = self.repo.commit(commit_id).committed_date
            prev_date = datetime.fromtimestamp(mktime(prev_struct_time))
            data['prev_date'] = prev_date

        Commit.objects.create(**data)
        #print('Commit code rate: {}'.format())

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
            #print('ID {}'.format(commit_id))
            self.pre_commit_checkout(commit_id, prev_commit_id)
            self.repo.git.checkout(commit_id)
            self.post_commit_checkout(commit_id, prev_commit_id)
            prev_commit_id = commit_id
        self.repo.git.checkout('master')
