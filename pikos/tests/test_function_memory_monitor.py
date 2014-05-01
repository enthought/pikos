# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: tests/test_function_memory_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import unittest

from pikos.recorders.list_recorder import ListRecorder
from pikos.filters.on_value import OnValue
from pikos.tests.test_assistant import TestAssistant
from pikos.tests.compat import TestCase


class TestFunctionMemoryMonitor(TestCase, TestAssistant):

    def setUp(self):
        self.check_for_psutils()
        from pikos.monitors.function_memory_monitor import (
            FunctionMemoryMonitor)
        self.monitor_type = FunctionMemoryMonitor
        self.filename = __file__.replace('.pyc', '.py')
        self.recorder = ListRecorder(
            filter_=OnValue('filename', self.filename))
        self.logger = self.monitor_type(self.recorder)

    def test_function(self):
        logger = self.logger
        recorder = self.recorder

        @logger.attach
        def gcd(x, y):
            while x > 0:
                x, y = y % x, x
            return y

        def boo():
            pass

        boo()
        result = gcd(12, 3)
        boo()
        self.assertEqual(result, 3)
        records = self.get_records(recorder)
        expected = [
            "3 call gcd 34 {0}".format(self.filename),
            "4 return gcd 38 {0}".format(self.filename)]
        self.assertEqual(records, expected)

    def test_recursive(self):
        logger = self.logger
        recorder = self.recorder

        @logger.attach
        def gcd(x, y):
            return x if y == 0 else gcd(y, (x % y))

        def boo():
            return gcd(7, 12)

        result = boo()

        self.assertEqual(result, 1)
        records = self.get_records(recorder)
        expected = [
            "3 call gcd 57 {0}".format(self.filename),
            "11 call gcd 57 {0}".format(self.filename),
            "19 call gcd 57 {0}".format(self.filename),
            "27 call gcd 57 {0}".format(self.filename),
            "35 call gcd 57 {0}".format(self.filename),
            "43 call gcd 57 {0}".format(self.filename),
            "44 return gcd 59 {0}".format(self.filename),
            "52 return gcd 59 {0}".format(self.filename),
            "60 return gcd 59 {0}".format(self.filename),
            "68 return gcd 59 {0}".format(self.filename),
            "76 return gcd 59 {0}".format(self.filename),
            "84 return gcd 59 {0}".format(self.filename)]
        self.assertEqual(records, expected)

    def test_generator(self):
        logger = self.logger
        recorder = self.recorder
        output = (0, 1, 1, 2, 3, 5, 8, 13, 21, 34)

        @logger.attach
        def fibonacci(items):
            x, y = 0, 1
            for i in range(items):
                yield x
                x, y = y, x + y

        def boo():
            pass

        boo()
        result = [value for value in fibonacci(10)]
        boo()
        self.assertSequenceEqual(result, output)
        records = self.get_records(recorder)
        expected = [
            "3 call fibonacci 88 {0}".format(self.filename),
            "4 c_call range 91 {0}".format(self.filename),
            "5 c_return range 91 {0}".format(self.filename),
            "6 return fibonacci 92 {0}".format(self.filename),
            "19 call fibonacci 92 {0}".format(self.filename),
            "20 return fibonacci 92 {0}".format(self.filename),
            "34 call fibonacci 92 {0}".format(self.filename),
            "35 return fibonacci 92 {0}".format(self.filename),
            "49 call fibonacci 92 {0}".format(self.filename),
            "50 return fibonacci 92 {0}".format(self.filename),
            "64 call fibonacci 92 {0}".format(self.filename),
            "65 return fibonacci 92 {0}".format(self.filename),
            "79 call fibonacci 92 {0}".format(self.filename),
            "80 return fibonacci 92 {0}".format(self.filename),
            "94 call fibonacci 92 {0}".format(self.filename),
            "95 return fibonacci 92 {0}".format(self.filename),
            "109 call fibonacci 92 {0}".format(self.filename),
            "110 return fibonacci 92 {0}".format(self.filename),
            "124 call fibonacci 92 {0}".format(self.filename),
            "125 return fibonacci 92 {0}".format(self.filename),
            "139 call fibonacci 92 {0}".format(self.filename),
            "140 return fibonacci 92 {0}".format(self.filename),
            "154 call fibonacci 92 {0}".format(self.filename),
            "155 return fibonacci 93 {0}".format(self.filename)]
        self.assertEqual(records, expected)

    def test_function_using_tuples(self):
        # tuple records are not compatible with the default OnValue filters.
        recorder = ListRecorder(filter_=lambda x: x[-1] == self.filename)
        logger = self.monitor_type(recorder, record_type=tuple)

        @logger.attach
        def gcd(x, y):
            while x > 0:
                x, y = y % x, x
            return y

        def boo():
            pass

        boo()
        result = gcd(12, 3)
        boo()
        self.assertEqual(result, 3)
        expected = [
            "3 call gcd 135 {0}".format(self.filename),
            "4 return gcd 139 {0}".format(self.filename)]
        records = self.get_records(recorder)
        self.assertEqual(records, expected)

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
