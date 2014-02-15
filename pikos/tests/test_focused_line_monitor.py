# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/test_focused_line_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import StringIO
import unittest

from pikos.monitors.focused_line_monitor import FocusedLineMonitor
from pikos.recorders.api import TextStreamRecorder
from pikos.tests.test_assistant import TestAssistant
from pikos.tests.compat import TestCase


class TestFocusedLineMonitor(TestCase, TestAssistant):

    def setUp(self):
        self.filename = __file__.replace('.pyc', '.py')
        self.maxDiff = None
        self.stream = StringIO.StringIO()
        self.recorder = TextStreamRecorder(text_stream=self.stream)

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
        logger = FocusedLineMonitor(recorder, functions=[gcd])

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

        filename = self.filename
        expected = [
            "index function lineNo line filename",
            "-----------------------------------",
            "0 gcd 30             while x > 0: {0}".format(filename),
            "1 gcd 31                 x, y = internal(x, y) {0}".format(filename),
            "2 gcd 30             while x > 0: {0}".format(filename),
            "3 gcd 31                 x, y = internal(x, y) {0}".format(filename),
            "4 gcd 30             while x > 0: {0}".format(filename),
            "5 gcd 32             return y {0}".format(filename)]
        records = ''.join(self.stream.buflist).splitlines()
        self.assertEqual(records, expected)

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
        logger = FocusedLineMonitor(recorder, functions=[gcd, foo])

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
        filename = self.filename
        expected = [
            "index function lineNo line filename",
            "-----------------------------------",
            "0 gcd 72             while x > 0: {0}".format(filename),
            "1 gcd 73                 x, y = internal(x, y) {0}".format(filename),
            "2 gcd 72             while x > 0: {0}".format(filename),
            "3 gcd 73                 x, y = internal(x, y) {0}".format(filename),
            "4 gcd 72             while x > 0: {0}".format(filename),
            "5 gcd 74             return y {0}".format(filename),
            "6 foo 83             boo() {0}".format(filename),
            "7 foo 84             boo() {0}".format(filename)]
        records = ''.join(self.stream.buflist).splitlines()
        self.assertEqual(records, expected)

    def test_focus_on_recursive(self):

        def gcd(x, y):
            foo()
            return x if y == 0 else gcd(y, (x % y))

        def boo():
            pass

        def foo():
            pass

        recorder = self.recorder
        logger = FocusedLineMonitor(recorder, functions=[gcd])

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
        filename = self.filename
        expected = [
            "index function lineNo line filename",
            "-----------------------------------",
            "0 gcd 119             foo() {0}".format(filename),
            "1 gcd 120             return x if y == 0 else gcd(y, (x % y)) {0}".format(filename),
            "2 gcd 119             foo() {0}".format(filename),
            "3 gcd 120             return x if y == 0 else gcd(y, (x % y)) {0}".format(filename)]
        records = ''.join(self.stream.buflist).splitlines()
        self.assertEqual(records, expected)

    def test_focus_on_decorated_recursive_function(self):

        def foo():
            pass

        recorder = ListRecorder()
        logger = FocusedLineMonitor(recorder)

        @logger.attach(include_decorated=True)
        def gcd(x, y):
            foo()
            return x if y == 0 else gcd(y, (x % y))

        result = gcd(12, 3)
        self.assertEqual(result, 3)
        records = recorder.records
        expected = [LineRecord(index=0, function='gcd', lineNo=187,
                               line='            foo()',
                               filename=self.filename),
                    LineRecord(index=1, function='gcd', lineNo=188,
                               line='            return x if y == 0 else '
                                    'gcd(y, (x % y))',
                               filename=self.filename),
                    LineRecord(index=2, function='gcd', lineNo=187,
                               line='            foo()',
                               filename=self.filename),
                    LineRecord(index=3, function='gcd',  lineNo=188,
                               line='            return x if y == 0 else '
                                    'gcd(y, (x % y))',
                               filename=self.filename)]
        self.assertEqual(records, expected)

    def test_focus_on_decorated_function(self):

        def internal(x, y):
            return y % x, x

        def boo():
            pass

        def foo():
            boo()
            boo()

        recorder = ListRecorder()
        logger = FocusedLineMonitor(recorder)

        @logger.attach(include_decorated=True)
        def gcd(x, y):
            while x > 0:
                x, y = internal(x, y)
            return y

        boo()
        result = gcd(12, 3)
        boo()
        self.assertEqual(result, 3)
        records = recorder.records
        expected = [LineRecord(index=0, function='gcd', lineNo=226,
                               line='            while x > 0:',
                               filename=self.filename),
                    LineRecord(index=1, function='gcd', lineNo=227,
                               line='                x, y = internal(x, y)',
                               filename=self.filename),
                    LineRecord(index=2, function='gcd', lineNo=226,
                               line='            while x > 0:',
                               filename=self.filename),
                    LineRecord(index=3, function='gcd', lineNo=227,
                               line='                x, y = internal(x, y)',
                               filename=self.filename),
                    LineRecord(index=4, function='gcd', lineNo=226,
                               line='            while x > 0:',
                               filename=self.filename),
                    LineRecord(index=5, function='gcd', lineNo=228,
                               line='            return y',
                               filename=self.filename)]
        self.assertEqual(records, expected)


if __name__ == '__main__':
    unittest.main()
