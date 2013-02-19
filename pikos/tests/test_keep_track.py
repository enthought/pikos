import unittest

from pikos._internal.keep_track import KeepTrack
from pikos.tests.compat import TestCase


class TestKeepTrack(TestCase):

    def test_lifetime(self):
        my_class = KeepTrack()
        self.assertTrue(my_class())
        self.assertFalse(my_class('ping'))
        self.assertFalse(my_class('ping'))
        self.assertFalse(my_class('pong'))
        self.assertFalse(my_class('pong'))
        self.assertTrue(my_class('pong'))
        self.assertTrue(my_class('ping'))
        self.assertFalse(my_class('ping'))
        self.assertFalse(my_class('pong'))
        self.assertTrue(my_class('pong'))
        self.assertFalse(my_class('pong'))
        self.assertTrue(my_class())

    def test_boolean_evaluation(self):
        my_class = KeepTrack()
        self.assertFalse(my_class)
        my_class()
        self.assertTrue(my_class)
        my_class('ping')
        self.assertTrue(my_class)
        my_class('pong')
        self.assertTrue(my_class)
        my_class('pong')
        self.assertFalse(my_class)
        my_class('pong')
        self.assertFalse(my_class)


if __name__ == '__main__':
    unittest.main()
