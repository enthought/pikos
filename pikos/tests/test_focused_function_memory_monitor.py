# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/test_focused_function_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import unittest

from pikos.filters.on_value import OnValue
from pikos.monitors.focused_function_memory_monitor import (
    FocusedFunctionMemoryMonitor)
from pikos.recorders.list_recorder import ListRecorder
from pikos.monitors.function_memory_monitor import FunctionMemoryRecord
from pikos.tests.test_assistant import TestAssistant
from pikos.tests.compat import TestCase


class TestFocusedFunctionMemoryMonitor(TestCase, TestAssistant):

    def test_focus_on_function(self):

        def gcd(x, y):
            while x > 0:
                x, y = internal(x, y)
            return y

        def internal(x, y):
            return y % x, x

        def boo():
            pass

        recorder = ListRecorder()
        logger = FocusedFunctionMemoryMonitor(recorder, functions=[gcd])

        @logger.attach
        def container(x, y):
            boo()
            result = gcd(x, y)
            boo()
            return result

        boo()
        result = container(12, 3)
        boo()
        self.assertEqual(result, 3)
        records = recorder.records
        # check that the records make sense
        self.assertFieldValueExist(records, ('function', 'type'),
                                   ('gcd', 'call'), times=1)
        self.assertFieldValueExist(records, ('function', 'type'),
                                   ('gcd', 'return'), times=1)
        self.assertFieldValueExist(records, ('function', 'type'),
                                   ('internal', 'call'), times=2)
        self.assertFieldValueExist(records, ('function', 'type'),
                                   ('internal', 'return'), times=2)
        self.assertFieldValueNotExist(records, ('function',), ('boo',))
        # The wrapper of the function should not be logged
        self.assertFieldValueNotExist(records, ('function',), ('wrapper',))
        self.assertEqual(logger._code_trackers, {})

    def test_focus_on_functions(self):

        def gcd(x, y):
            while x > 0:
                x, y = internal(x, y)
            return y

        def internal(x, y):
            return y % x, x

        def boo():
            pass

        def foo():
            boo()
            boo()
            boo()

        recorder = ListRecorder()
        logger = FocusedFunctionMemoryMonitor(
            recorder, functions=[internal, foo])

        @logger.attach
        def container(x, y):
            boo()
            result = gcd(x, y)
            boo()
            foo()
            return result

        boo()
        result = container(12, 3)
        boo()
        self.assertEqual(result, 3)
        records = recorder.records
        # check that the records make sense
        self.assertFieldValueExist(records, ('function', 'type'),
                                   ('internal', 'call'), times=2)
        self.assertFieldValueExist(records, ('function', 'type'),
                                   ('internal', 'return'), times=2)
        self.assertFieldValueExist(records, ('function', 'type'),
                                   ('foo', 'call'), times=1)
        self.assertFieldValueExist(records, ('function', 'type'),
                                   ('foo', 'return'), times=1)
        self.assertFieldValueExist(records, ('function', 'type'),
                                   ('boo', 'call'), times=3)
        self.assertFieldValueExist(records, ('function', 'type'),
                                   ('boo', 'return'), times=3)
        self.assertFieldValueNotExist(records, ('function',), ('gcd',))
        # The wrapper of the function should not be logged
        self.assertFieldValueNotExist(records, ('function',), ('wrapper',))
        self.assertEqual(logger._code_trackers, {})

    def test_focus_on_recursive(self):

        def gcd(x, y):
            foo()
            return x if y == 0 else gcd(y, (x % y))

        def boo():
            pass

        def foo():
            pass

        recorder = ListRecorder()
        logger = FocusedFunctionMemoryMonitor(recorder, functions=[gcd])

        @logger.attach
        def container(x, y):
            boo()
            result = gcd(x, y)
            boo()
            foo()
            return result

        boo()
        result = container(12, 3)
        boo()
        self.assertEqual(result, 3)
        records = recorder.records
        # check that the records make sense
        self.assertFieldValueExist(records, ('function', 'type'),
                                   ('gcd', 'call'), times=2)
        self.assertFieldValueExist(records, ('function', 'type'),
                                   ('gcd', 'return'), times=2)
        self.assertFieldValueExist(records, ('function', 'type'),
                                   ('foo', 'call'), times=2)
        self.assertFieldValueExist(records, ('function', 'type'),
                                   ('foo', 'return'), times=2)
        self.assertFieldValueNotExist(records, ('function',), ('boo',))
        # The wrapper of the function should not be logged
        self.assertFieldValueNotExist(records, ('function',), ('wrapper',))
        self.assertEqual(logger._code_trackers, {})

    def test_focus_on_decorated_recursive(self):

        def foo():
            pass

        recorder = ListRecorder()
        logger = FocusedFunctionMemoryMonitor(recorder)

        @logger.attach(include_decorated=True)
        def gcd(x, y):
            foo()
            return x if y == 0 else gcd(y, (x % y))

        result = gcd(12, 3)
        self.assertEqual(result, 3)
        records = recorder.records
        # check that the records make sense
        self.assertFieldValueExist(records, ('function', 'type'),
                                   ('gcd', 'call'), times=2)
        self.assertFieldValueExist(records, ('function', 'type'),
                                   ('gcd', 'return'), times=2)
        self.assertFieldValueExist(records, ('function', 'type'),
                                   ('foo', 'call'), times=2)
        self.assertFieldValueExist(records, ('function', 'type'),
                                   ('foo', 'return'), times=2)
        self.assertFieldValueNotExist(records, ('function',), ('boo',))
        # FIXME: In decorated recursive case calls the wrapper of the function
        #        is logged self.assertFieldValueNotExist(records,
        #        ('function',), ('wrapper',))
        self.assertEqual(logger._code_trackers, {})


if __name__ == '__main__':
    unittest.main()
