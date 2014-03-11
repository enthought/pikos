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
from pikos.tests.compat import TestCase


class TestFocusedFunctionMemoryMonitor(TestCase):

    def setUp(self):
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
        expected = [
            "0 call gcd 28 {0}".format(self.filename),
            "1 call internal 33 {0}".format(self.filename),
            "2 return internal 34 {0}".format(self.filename),
            "3 call internal 33 {0}".format(self.filename),
            "4 return internal 34 {0}".format(self.filename),
            "5 return gcd 31 {0}".format(self.filename)]
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
        expected = [
            "0 call internal 71 {0}".format(self.filename),
            "1 return internal 72 {0}".format(self.filename),
            "2 call internal 71 {0}".format(self.filename),
            "3 return internal 72 {0}".format(self.filename),
            "4 call foo 77 {0}".format(self.filename),
            "5 call boo 74 {0}".format(self.filename),
            "6 return boo 75 {0}".format(self.filename),
            "7 call boo 74 {0}".format(self.filename),
            "8 return boo 75 {0}".format(self.filename),
            "9 call boo 74 {0}".format(self.filename),
            "10 return boo 75 {0}".format(self.filename),
            "11 return foo 80 {0}".format(self.filename)]
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
        expected = [
            "0 call gcd 117 {0}".format(self.filename),
            "1 call foo 124 {0}".format(self.filename),
            "2 return foo 125 {0}".format(self.filename),
            "3 call gcd 117 {0}".format(self.filename),
            "4 call foo 124 {0}".format(self.filename),
            "5 return foo 125 {0}".format(self.filename),
            "6 return gcd 119 {0}".format(self.filename),
            "7 return gcd 119 {0}".format(self.filename)]
        records = self.get_records(recorder)
        self.assertEqual(records, expected)
        self.assertEqual(logger._code_trackers, {})

    def test_focus_on_decorated_recursive(self):

        def foo():
            pass

        recorder = ListRecorder(filter_=OnValue('filename', self.filename))
        logger = FocusedFunctionMemoryMonitor(recorder)

        @logger.attach(include_decorated=True)
        def gcd(x, y):
            foo()
            return x if y == 0 else gcd(y, (x % y))

        result = gcd(12, 3)
        self.assertEqual(result, 3)
        expected = [
            "0 call gcd 163 {0}".format(self.filename),
            "1 call foo 157 {0}".format(self.filename),
            "2 return foo 158 {0}".format(self.filename),
            "10 call gcd 163 {0}".format(self.filename),
            "11 call foo 157 {0}".format(self.filename),
            "12 return foo 158 {0}".format(self.filename),
            "13 return gcd 166 {0}".format(self.filename),
            "21 return gcd 166 {0}".format(self.filename)]
        records = self.get_records(recorder)
        self.assertEqual(records, expected)
        self.assertEqual(logger._code_trackers, {})

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
        logger = FocusedFunctionMemoryMonitor(
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
            "0 call gcd 185 {0}".format(self.filename),
            "1 call internal 190 {0}".format(self.filename),
            "2 return internal 191 {0}".format(self.filename),
            "3 call internal 190 {0}".format(self.filename),
            "4 return internal 191 {0}".format(self.filename),
            "5 return gcd 188 {0}".format(self.filename)]
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


if __name__ == '__main__':
    unittest.main()
