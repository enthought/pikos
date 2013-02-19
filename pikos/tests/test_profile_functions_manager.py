import sys
import unittest

from pikos._internal.profile_function_manager import ProfileFunctionManager
from pikos.tests.compat import TestCase


class MockNativeMonitor():

    def __init__(self):
        self._profile = ProfileFunctionManager()

    def __enter__(self):
        self._profile.replace(self.event)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._profile.recover()

    def event(self, frame, event, arg):
        pass


class TestProfileFunctionsManager(TestCase):

    def setUp(self):
        self.old = sys.getprofile()

        def foo():
            pass

        def bar(frame, event, arg):
            pass
        self.foo = foo
        self.bar = bar
        self.monitor = MockNativeMonitor()

    def test_preserving_previous_function(self):

        sys.setprofile(self.bar)
        with self.monitor:
            self.foo()
        self.assertIs(sys.getprofile(), self.bar)

    def test_error_when_set_multiple(self):
        self.monitor._profile.replace(self.bar)
        self.assertIs(sys.getprofile(), self.bar)
        with self.assertRaises(AssertionError):
            with self.assertRaises(RuntimeError):
                self.monitor._profile.replace(self.bar)
                self.assertIs(sys.getprofile(), self.bar)
                self.monitor._profile.recover()

        self.monitor._profile.replace(self.bar)
        self.assertIs(sys.getprofile(), self.bar)
        with self.assertRaises(RuntimeError):
            self.monitor._profile.replace(None)
            self.assertIs(sys.getprofile(), self.bar)
        self.monitor._profile.recover()

    def test_error_when_unset(self):
        with self.assertRaises(RuntimeError):
            self.monitor._profile.recover()

    def tearDown(self):
        sys.setprofile(self.old)

if __name__ == '__main__':
    unittest.main()
