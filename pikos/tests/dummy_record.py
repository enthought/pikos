import os
from collections import namedtuple


class DummyRecord(namedtuple('DummyRecord', ('one', 'two', 'three'))):
    """ Dummy record used for testing.

    """

    @classmethod
    def header(cls):
        return '{0:<5} {1:<5} {2:<5}{newline}'.format(
            *cls._fields, newline=os.linesep)

    def line(self):
        return '{0:<5} {1:<5} {2:<5}{newline}'.format(
            *self, newline=os.linesep)
