from operator import or_, and_
import json
from django.db.models import Q
from commits.models import Commit


class HandBages(object):
    def __init__(self, bage_terms):
        self.bage_terms = bage_terms

    def get_commits(self):
        q = self.build_query(self.bage_terms.items())
        return Commit.objects.filter(q)

    def build_query(self, bage_terms):
        conn_type = None
        q = Q()
        for data in bage_terms:
            key = data[0]
            value = data[1]

            if key == '$or':
                conn_type = Q.OR
            elif key == '$and':
                conn_type = Q.AND

            for t in value.items():
                q.add(self.build_Q(t[0], t[1]), conn_type)
        return q

    def build_Q(self, key, value):
        return Q(**dict(((key, value),)))