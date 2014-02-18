# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/test_focused_function_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import StringIO
import unittest

from pikos.filters.on_value import OnValue
from pikos.monitors.focused_function_monitor import FocusedFunctionMonitor
from pikos.recorders.text_stream_recorder import TextStreamRecorder
from pikos.tests.compat import TestCase


class TestFocusedFunctionMonitor(TestCase):

    def setUp(self):
        self.maxDiff = None
        self.filename = __file__.replace('.pyc', '.py')
        self.stream = StringIO.StringIO()
        # we only care about the lines that are in this file and we filter
        # the others.
        self.recorder = TextStreamRecorder(
            text_stream=self.stream,
            filter_=OnValue('filename', self.filename))
        self.logger = FocusedFunctionMonitor(self.recorder)

    def test_focus_on_function(self):

        def gcd(x, y):
            while x > 0:
                x, y = internal(x, y)
            return y

        def internal(x, y):
            boo()
            return y % x, x

        def boo():
            pass

        recorder = self.recorder
        logger = FocusedFunctionMonitor(recorder, functions=[gcd])

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
            "index type function lineNo filename",
            "-----------------------------------",
            "0 call gcd 34 {0}".format(self.filename),
            "1 call internal 39 {0}".format(self.filename),
            "2 call boo 43 {0}".format(self.filename),
            "3 return boo 44 {0}".format(self.filename),
            "4 return internal 41 {0}".format(self.filename),
            "5 call internal 39 {0}".format(self.filename),
            "6 call boo 43 {0}".format(self.filename),
            "7 return boo 44 {0}".format(self.filename),
            "8 return internal 41 {0}".format(self.filename),
            "9 return gcd 37 {0}".format(self.filename),]
        records = ''.join(self.stream.buflist).splitlines()
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

        recorder = self.recorder
        logger = FocusedFunctionMonitor(recorder, functions=[gcd, foo])

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
            "index type function lineNo filename",
            "-----------------------------------",
            "0 call gcd 79 {0}".format(self.filename),
            "1 call internal 84 {0}".format(self.filename),
            "2 return internal 85 {0}".format(self.filename),
            "3 call internal 84 {0}".format(self.filename),
            "4 return internal 85 {0}".format(self.filename),
            "5 return gcd 82 {0}".format(self.filename),        
            "6 call foo 90 {0}".format(self.filename),
            "7 call boo 87 {0}".format(self.filename),
            "8 return boo 88 {0}".format(self.filename),
            "9 call boo 87 {0}".format(self.filename),
            "10 return boo 88 {0}".format(self.filename),
            "11 return foo 92 {0}".format(self.filename),
        ]
        records = ''.join(self.stream.buflist).splitlines()
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
        logger = FocusedFunctionMonitor(recorder, functions=[gcd])

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
            "index type function lineNo filename",
            "-----------------------------------",
            "0 call gcd 131 {0}".format(self.filename),
            "1 call foo 138 {0}".format(self.filename),
            "2 return foo 139 {0}".format(self.filename),
            "3 call gcd 131 {0}".format(self.filename),
            "4 call foo 138 {0}".format(self.filename),
            "5 return foo 139 {0}".format(self.filename),
            "6 return gcd 133 {0}".format(self.filename),
            "7 return gcd 133 {0}".format(self.filename),]
        records = ''.join(self.stream.buflist).splitlines()
        self.assertEqual(records, expected)
        self.assertEqual(logger._code_trackers, {})

    def test_focus_on_decorated_recursive(self):

        def foo():
            pass

        recorder = TextStreamRecorder(
            self.stream, filter_=OnValue('filename', self.filename))
        logger = FocusedFunctionMonitor(recorder)

        @logger.attach(include_decorated=True)
        def gcd(x, y):
            foo()
            return x if y == 0 else gcd(y, (x % y))

        result = gcd(12, 3)
        self.assertEqual(result, 3)
        expected = [
            "index type function lineNo filename",
            "-----------------------------------",
            "0 call gcd 180 {0}".format(self.filename),
            "1 call foo 173 {0}".format(self.filename),
            "2 return foo 174 {0}".format(self.filename),
            "10 call gcd 180 {0}".format(self.filename),
            "11 call foo 173 {0}".format(self.filename),
            "12 return foo 174 {0}".format(self.filename),
            "13 return gcd 183 {0}".format(self.filename),
            "21 return gcd 183 {0}".format(self.filename)]
        records = ''.join(self.stream.buflist).splitlines()
        self.assertEqual(records, expected)
        self.assertEqual(logger._code_trackers, {})

    def test_focus_on_decorated_function(self):

        def gcd(x, y):
            while x > 0:
                x, y = internal(x, y)
            return y

        def internal(x, y):
            boo()
            return y % x, x

        def boo():
            pass

        recorder = self.recorder
        logger = FocusedFunctionMonitor(recorder)

        @logger.attach(include_decorated=True)
        def container(x, y):
            result = gcd(x, y)
            boo()
            return result

        boo()
        result = container(12, 3)
        boo()
        self.assertEqual(result, 3)
        expected = [
            "index type function lineNo filename",
            "-----------------------------------",
            "0 call container 219 {0}".format(self.filename),
            "1 call gcd 204 {0}".format(self.filename),
            "2 call internal 209 {0}".format(self.filename),
            "3 call boo 213 {0}".format(self.filename),
            "4 return boo 214 {0}".format(self.filename),
            "5 return internal 211 {0}".format(self.filename),
            "6 call internal 209 {0}".format(self.filename),
            "7 call boo 213 {0}".format(self.filename),
            "8 return boo 214 {0}".format(self.filename),
            "9 return internal 211 {0}".format(self.filename),
            "10 return gcd 207 {0}".format(self.filename),
            "11 call boo 213 {0}".format(self.filename),
            "12 return boo 214 {0}".format(self.filename),
            "13 return container 223 {0}".format(self.filename),]
        records = ''.join(self.stream.buflist).splitlines()
        self.assertEqual(records, expected)
        self.assertEqual(logger._code_trackers, {})


if __name__ == '__main__':
    unittest.main()
