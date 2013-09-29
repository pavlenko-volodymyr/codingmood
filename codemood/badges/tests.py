import datetime
from django.db.models import Q
from django.test import TestCase

import factory as factory_boy

from commits.models import Commit, Repository
from common.factories import UserFactory
from .hand import HandBages


class RepositoryFactory(factory_boy.DjangoModelFactory):
    FACTORY_FOR = Repository
    user = factory_boy.LazyAttribute(lambda a: UserFactory())
    title = 'title'
    url = 'url'

class CommitFactory(factory_boy.DjangoModelFactory):
    FACTORY_FOR = Commit
    commit_id = 1

    code_rate = 10.0

    date = datetime.datetime.now()

    messages = 'Message'

    author = 'Author'
    author_email = 'author@example.com'

    cyclomatic_complexity = 1
    cyclomatic_complexity_rank = 'A'

    n_of_row_added = 1
    n_of_row_deleted = 2

    repository = factory_boy.LazyAttribute(lambda a: RepositoryFactory())


class HandBagesTest(TestCase):
    def test_basic_addition(self):
        CommitFactory.create()

        data_to_query = {"$and": {"code_rate__gte": 9}}
        hand_bages = HandBages(data_to_query)
        self.assertEqual(hand_bages.get_commits().count(), 1)

        data_to_query = {"$or": {"code_rate__gte": 20, 'n_of_row_added': 1}}
        hand_bages = HandBages(data_to_query)
        self.assertEqual(hand_bages.get_commits().count(), 1)