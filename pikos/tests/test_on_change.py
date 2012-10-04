import unittest
import collections

from pikos.filters.on_change import OnChange

MockRecord = collections.namedtuple('MockRecord',
                                    ['function', 'filename', 'line'])


class TestOnChange(unittest.TestCase):

    def test_initialization(self):

        my_filter = OnChange('function')
        self.assertEqual(my_filter.field, 'function')
        self.assertIsNone(my_filter.previous)

    def test_call(self):

        my_filter = OnChange('filename')
        record = MockRecord('foo', 'bar.py', 3)
        self.assertTrue(my_filter(record))
        record = MockRecord('bar', 'foo.py', 7)
        self.assertTrue(my_filter(record))
        record = MockRecord('foo', 'foo.py', 123)
        self.assertFalse(my_filter(record))


if __name__ == '__main__':
    unittest.main()
