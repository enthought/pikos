import sys
import unittest

from pikos._internal.trace_function_manager import TraceFunctionManager
from pikos.tests.compat import TestCase


class MockNativeMonitor():

    def __init__(self):
        self._profile = TraceFunctionManager()

    def __enter__(self):
        self._profile.replace(self.event)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._profile.recover()

    def event(self, frame, event, arg):
        return self.event


class TestTraceFunctionsManager(TestCase):

    def setUp(self):
        self.old = sys.gettrace()

        def foo():
            pass

        def bar(frame, event, arg):
            pass
        self.foo = foo
        self.bar = bar
        self.monitor = MockNativeMonitor()

    def tearDown(self):
        sys.settrace(self.old)

    def test_preserving_previous_function(self):

        sys.settrace(self.bar)
        with self.monitor:
            self.foo()
        self.assertIs(sys.gettrace(), self.bar)

    def test_error_when_set_multiple(self):
        self.monitor._profile.replace(self.bar)
        self.assertIs(sys.gettrace(), self.bar)
        self.monitor._profile.replace(self.bar)
        self.assertIs(sys.gettrace(), self.bar)
        self.monitor._profile.recover()

        self.monitor._profile.replace(self.bar)
        self.assertIs(sys.gettrace(), self.bar)
        with self.assertRaises(RuntimeError):
            self.monitor._profile.replace(None)
            self.assertIs(sys.gettrace(), self.bar)
        self.monitor._profile.recover()
        self.assertIs(sys.gettrace(), self.old)

    def test_error_when_unset(self):
        with self.assertRaises(RuntimeError):
            self.monitor._profile.recover()
        self.assertIs(sys.gettrace(), self.old)


if __name__ == '__main__':
    unittest.main()
