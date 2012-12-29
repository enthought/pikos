# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/line_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import unittest

from pikos.monitors.focused_line_monitor import FocusedLineMonitor
from pikos.recorders.list_recorder import ListRecorder
from pikos.monitors.line_monitor import LineRecord
from pikos.tests.test_assistant import TestAssistant


class TestFocusedLineMonitor(unittest.TestCase, TestAssistant):

    def setUp(self):
        self.filename = __file__.replace('.pyc', '.py')
        self.maxDiff = None

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

        recorder = ListRecorder()
        logger = FocusedLineMonitor(recorder, [gcd])

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
        expected = [LineRecord(index=0, function='gcd', lineNo=27,
                               line='            while x > 0:',
                               filename=self.filename),
                    LineRecord(index=1, function='gcd', lineNo=28,
                               line='                x, y = internal(x, y)',
                               filename=self.filename),
                    LineRecord(index=2, function='gcd', lineNo=27,
                               line='            while x > 0:',
                               filename=self.filename),
                    LineRecord(index=3, function='gcd', lineNo=28,
                               line='                x, y = internal(x, y)',
                               filename=self.filename),
                    LineRecord(index=4, function='gcd', lineNo=27,
                               line='            while x > 0:',
                               filename=self.filename),
                    LineRecord(index=5, function='gcd', lineNo=29,
                               line='            return y',
                               filename=self.filename)]
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

        recorder = ListRecorder()
        logger = FocusedLineMonitor(recorder, [gcd, foo])

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
        expected = [LineRecord(index=0, function='gcd', lineNo=76,
                               line='            while x > 0:',
                               filename=self.filename),
                    LineRecord(index=1, function='gcd', lineNo=77,
                               line='                x, y = internal(x, y)',
                               filename=self.filename),
                    LineRecord(index=2, function='gcd', lineNo=76,
                               line='            while x > 0:',
                               filename=self.filename),
                    LineRecord(index=3, function='gcd', lineNo=77,
                               line='                x, y = internal(x, y)',
                               filename=self.filename),
                    LineRecord(index=4, function='gcd', lineNo=76,
                               line='            while x > 0:',
                               filename=self.filename),
                    LineRecord(index=5, function='gcd', lineNo=78,
                               line='            return y',
                               filename=self.filename),
                    LineRecord(index=6, function='foo', lineNo=87,
                               line='            boo()',
                               filename=self.filename),
                    LineRecord(index=7, function='foo', lineNo=88,
                               line='            boo()',
                               filename=self.filename)]
        self.assertEqual(records, expected)

    def test_focus_on_recursive(self):

        def gcd(x, y):
            foo()
            return x if y == 0 else gcd(y, (x % y))

        def boo():
            pass

        def foo():
            pass

        recorder = ListRecorder()
        logger = FocusedLineMonitor(recorder, [gcd])

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
        expected = [LineRecord(index=0, function='gcd', lineNo=135,
                               line='            foo()',
                               filename=self.filename),
                    LineRecord(index=1, function='gcd', lineNo=136,
                               line='            return x if y == 0 else '
                                    'gcd(y, (x % y))',
                               filename=self.filename),
                    LineRecord(index=2, function='gcd', lineNo=135,
                               line='            foo()',
                               filename=self.filename),
                    LineRecord(index=3, function='gcd',  lineNo=136,
                               line='            return x if y == 0 else '
                                    'gcd(y, (x % y))',
                               filename=self.filename)]
        self.assertEqual(records, expected)

if __name__ == '__main__':
    unittest.main()
