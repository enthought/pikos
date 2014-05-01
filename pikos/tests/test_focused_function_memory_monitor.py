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
from pikos.recorders.list_recorder import ListRecorder
from pikos.tests.compat import TestCase


class TestFocusedFunctionMemoryMonitor(TestCase):

    def setUp(self):
        self.check_for_psutils()
        from pikos.monitors.focused_function_memory_monitor import (
            FocusedFunctionMemoryMonitor)
        self.monitor_type = FocusedFunctionMemoryMonitor
        self.filename = __file__.replace('.pyc', '.py')
        self.maxDiff = None
        self.recorder = ListRecorder()

    def test_focus_on_function(self):

        def gcd(x, y):
            while x > 0:
                x, y = internal(x, y)
            return y

        def internal(x, y):
            return y % x, x

        def boo():
            pass

        recorder = self.recorder
        logger = self.monitor_type(recorder, functions=[gcd])

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
        expected = [
            "0 call gcd 30 {0}".format(self.filename),
            "1 call internal 35 {0}".format(self.filename),
            "2 return internal 36 {0}".format(self.filename),
            "3 call internal 35 {0}".format(self.filename),
            "4 return internal 36 {0}".format(self.filename),
            "5 return gcd 33 {0}".format(self.filename)]
        records = self.get_records(recorder)
        self.assertEqual(records, expected)
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

        recorder = self.recorder
        logger = self.monitor_type(
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
        expected = [
            "0 call internal 73 {0}".format(self.filename),
            "1 return internal 74 {0}".format(self.filename),
            "2 call internal 73 {0}".format(self.filename),
            "3 return internal 74 {0}".format(self.filename),
            "4 call foo 79 {0}".format(self.filename),
            "5 call boo 76 {0}".format(self.filename),
            "6 return boo 77 {0}".format(self.filename),
            "7 call boo 76 {0}".format(self.filename),
            "8 return boo 77 {0}".format(self.filename),
            "9 call boo 76 {0}".format(self.filename),
            "10 return boo 77 {0}".format(self.filename),
            "11 return foo 82 {0}".format(self.filename)]
        records = self.get_records(recorder)
        self.assertEqual(records, expected)
        self.assertEqual(logger._code_trackers, {})

    def test_focus_on_recursive(self):

        def gcd(x, y):
            foo()
            return x if y == 0 else gcd(y, (x % y))

        def boo():
            pass

        def foo():
            pass

        recorder = self.recorder
        logger = self.monitor_type(recorder, functions=[gcd])

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
        expected = [
            "0 call gcd 119 {0}".format(self.filename),
            "1 call foo 126 {0}".format(self.filename),
            "2 return foo 127 {0}".format(self.filename),
            "3 call gcd 119 {0}".format(self.filename),
            "4 call foo 126 {0}".format(self.filename),
            "5 return foo 127 {0}".format(self.filename),
            "6 return gcd 121 {0}".format(self.filename),
            "7 return gcd 121 {0}".format(self.filename)]
        records = self.get_records(recorder)
        self.assertEqual(records, expected)
        self.assertEqual(logger._code_trackers, {})

    def test_focus_on_decorated_recursive(self):

        def foo():
            pass

        recorder = ListRecorder(filter_=OnValue('filename', self.filename))
        logger = self.monitor_type(recorder)

        @logger.attach(include_decorated=True)
        def gcd(x, y):
            foo()
            return x if y == 0 else gcd(y, (x % y))

        result = gcd(12, 3)
        self.assertEqual(result, 3)
        expected = [
            "0 call gcd 165 {0}".format(self.filename),
            "1 call foo 159 {0}".format(self.filename),
            "2 return foo 160 {0}".format(self.filename),
            "10 call gcd 165 {0}".format(self.filename),
            "11 call foo 159 {0}".format(self.filename),
            "12 return foo 160 {0}".format(self.filename),
            "13 return gcd 168 {0}".format(self.filename),
            "21 return gcd 168 {0}".format(self.filename)]
        records = self.get_records(recorder)
        self.assertEqual(records, expected)
        self.assertEqual(logger._code_trackers, {})

    def test_focus_on_function_using_tuples(self):

        def gcd(x, y):
            while x > 0:
                x, y = internal(x, y)
            return y

        def internal(x, y):
            return y % x, x

        def boo():
            pass

        recorder = self.recorder
        logger = self.monitor_type(
            recorder, record_type=tuple, functions=[gcd])

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
        expected = [
            "0 call gcd 187 {0}".format(self.filename),
            "1 call internal 192 {0}".format(self.filename),
            "2 return internal 193 {0}".format(self.filename),
            "3 call internal 192 {0}".format(self.filename),
            "4 return internal 193 {0}".format(self.filename),
            "5 return gcd 190 {0}".format(self.filename)]
        records = self.get_records(recorder)
        self.assertEqual(records, expected)
        self.assertEqual(logger._code_trackers, {})

    def get_records(self, recorder):
        """ Remove the memory related fields.
        """
        records = []
        for record in recorder.records:
            filtered = record[:3] + record[5:]
            records.append(
                ' '.join([str(item).rstrip() for item in filtered]))
        return records

    def check_for_psutils(self):
        try:
            import psutil
        except ImportError:
            self.skipTest('Could not import psutils, skipping test.')


if __name__ == '__main__':
    unittest.main()
