from collections import namedtuple


class DummyRecord(namedtuple('DummyRecord', ('one', 'two', 'three'))):
    """ Dummy record used for testing.

    """

    __slots__ = ()

    header = u'{0:<5} {1:<5} {2:<5}'
    line = u'{0:<5} {1:<5} {2:<5}'
