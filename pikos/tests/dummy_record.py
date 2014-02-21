from collections import namedtuple


class DummyRecord(namedtuple('DummyRecord', ('one', 'two', 'three'))):
    """ Dummy record used for testing.

    """
    @classmethod
    def header(cls):
        return u'{0:<5} {1:<5} {2:<5}'.format(*cls._fields)

    def line(self):
        return u'{0:<5} {1:<5} {2:<5}'.format(*self)
