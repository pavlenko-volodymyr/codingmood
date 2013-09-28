import json
from django.db.models import Q


class HandBages(object):
    def __init__(self, bage_terms):
        test = map(self.build_Q, json.loads(bage_terms).iteritems())
        print test

    def build_Q(self, data):
        key = data[0]
        value = data[1]

        if '$' in key:
            if key == '$or':
                pass # or
            elif key == '$and':
                pass # and
            else:
                return '{0}={1}'.format(key, value).replace('$', '__')
        else:
            if type(value) is dict:
                if len(value) == 1:
                    return key + self.build_Q(value.items()[0])
                else:
                    raise Exception
            else:
                return '%s=%s' % (key, value)