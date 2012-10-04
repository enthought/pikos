import unittest
import collections

from pikos.filters.on_value import OnValue

MockRecord = collections.namedtuple('MockRecord',
                                    ['function', 'filename', 'line'])


class TestOnValue(unittest.TestCase):

    def test_initialization(self):

        my_filter = OnValue('function', 'foo')
        self.assertEqual(my_filter.values, ['foo'])

        my_filter = OnValue('filename', 'foo.py')
        self.assertEqual(my_filter.values, ['foo.py'])

    def test_call(self):

        my_filter = OnValue('function', 'bar')
        record = MockRecord('foo', 'bar.py', 3)
        self.assertFalse(my_filter(record))
        record = MockRecord('bar', 'foo.py', 7)
        self.assertTrue(my_filter(record))

        my_filter = OnValue('filename', 'bar.py', 'foo.py')
        record = MockRecord('foo', 'bar.py', 3)
        self.assertTrue(my_filter(record))
        record = MockRecord('f', 'foo.py', 3)
        self.assertTrue(my_filter(record))
        record = MockRecord('f', 'non_foo.py', 3)
        self.assertFalse(my_filter(record))

if __name__ == '__main__':
    unittest.main()
