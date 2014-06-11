# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: tests/test_line_memory_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
# -----------------------------------------------------------------------------
import unittest

from pikos.filters.on_value import OnValue
from pikos.tests.compat import TestCase
from pikos.tests.monitoring_helper import MonitoringHelper
from pikos.recorders.list_recorder import ListRecorder


class TestLineMemoryMonitor(TestCase):

    def setUp(self):
        self.check_for_psutils()
        from pikos.monitors.line_memory_monitor import LineMemoryMonitor
        self.maxDiff = None
        self.helper = MonitoringHelper()
        self.filename = self.helper.filename
        self.recorder = ListRecorder(
            filter_=OnValue('filename', self.filename))
        self.monitor = LineMemoryMonitor(self.recorder)
        self.helper.monitor = self.monitor

    def test_function(self):
        result = self.helper.run_on_function()
        self.assertEqual(result, 3)

        template = [
            "0 gcd 29             while x > 0: {0}",
            "1 gcd 30                 x, y = y % x, x {0}",
            "2 gcd 29             while x > 0: {0}",
            "3 gcd 30                 x, y = y % x, x {0}",
            "4 gcd 29             while x > 0: {0}",
            "5 gcd 31             return y {0}"]
        self.check_records(template, self.recorder)

    def test_recursive(self):
        result = self.helper.run_on_recursive_function()
        self.assertEqual(result, 1)

        template = [
            "0 gcd 49             return x if y == 0 else gcd(y, (x % y)) {0}",  # noqa
            "8 gcd 49             return x if y == 0 else gcd(y, (x % y)) {0}",  # noqa
            "16 gcd 49             return x if y == 0 else gcd(y, (x % y)) {0}",  # noqa
            "24 gcd 49             return x if y == 0 else gcd(y, (x % y)) {0}",  # noqa
            "32 gcd 49             return x if y == 0 else gcd(y, (x % y)) {0}",  # noqa
            "40 gcd 49             return x if y == 0 else gcd(y, (x % y)) {0}"]  # noqa
        self.check_records(template, self.recorder)

    def test_generator(self):
        result = self.helper.run_on_generator()
        output = (0, 1, 1, 2, 3, 5, 8, 13, 21, 34)
        self.assertSequenceEqual(result, output)

        template = [
            "0 fibonacci 64             x, y = 0, 1 {0}",
            "1 fibonacci 65             for i in range(items): {0}",  # noqa
            "2 fibonacci 66                 yield x {0}",
            "11 fibonacci 67                 x, y = y, x + y {0}",  # noqa
            "12 fibonacci 65             for i in range(items): {0}",  # noqa
            "13 fibonacci 66                 yield x {0}",
            "22 fibonacci 67                 x, y = y, x + y {0}",  # noqa
            "23 fibonacci 65             for i in range(items): {0}",  # noqa
            "24 fibonacci 66                 yield x {0}",
            "33 fibonacci 67                 x, y = y, x + y {0}",  # noqa
            "34 fibonacci 65             for i in range(items): {0}",  # noqa
            "35 fibonacci 66                 yield x {0}",
            "44 fibonacci 67                 x, y = y, x + y {0}",  # noqa
            "45 fibonacci 65             for i in range(items): {0}",  # noqa
            "46 fibonacci 66                 yield x {0}",
            "55 fibonacci 67                 x, y = y, x + y {0}",  # noqa
            "56 fibonacci 65             for i in range(items): {0}",  # noqa
            "57 fibonacci 66                 yield x {0}",
            "66 fibonacci 67                 x, y = y, x + y {0}",  # noqa
            "67 fibonacci 65             for i in range(items): {0}",  # noqa
            "68 fibonacci 66                 yield x {0}",
            "77 fibonacci 67                 x, y = y, x + y {0}",  # noqa
            "78 fibonacci 65             for i in range(items): {0}",  # noqa
            "79 fibonacci 66                 yield x {0}",
            "88 fibonacci 67                 x, y = y, x + y {0}",  # noqa
            "89 fibonacci 65             for i in range(items): {0}",  # noqa
            "90 fibonacci 66                 yield x {0}",
            "99 fibonacci 67                 x, y = y, x + y {0}",  # noqa
            "100 fibonacci 65             for i in range(items): {0}",  # noqa
            "101 fibonacci 66                 yield x {0}",
            "110 fibonacci 67                 x, y = y, x + y {0}",  # noqa
            "111 fibonacci 65             for i in range(items): {0}"]  # noqa

        self.check_records(template, self.recorder)

    def test_function_using_tuples(self):
        from pikos.monitors.line_memory_monitor import LineMemoryMonitor
        filename = self.filename
        # tuple records are not compatible with the default OnValue filters.
        recorder = ListRecorder(filter_=lambda x: x[-1] == filename)
        monitor = LineMemoryMonitor(recorder, record_type=tuple)
        helper = MonitoringHelper(monitor)
        result = helper.run_on_function()
        self.assertEqual(result, 3)
        template = [
            "0 gcd 29             while x > 0: {0}",
            "1 gcd 30                 x, y = y % x, x {0}",
            "2 gcd 29             while x > 0: {0}",
            "3 gcd 30                 x, y = y % x, x {0}",
            "4 gcd 29             while x > 0: {0}",
            "5 gcd 31             return y {0}"]
        self.check_records(template, recorder)

    def test_issue2(self):
        """ Test for issue #2.

        """
        monitor = self.monitor

        FOO = """
def foo():
    a = []
    for i in range(20):
        a.append(i+sum(a))

foo()
"""

        @monitor.attach
        def boo():
            code = compile(FOO, 'foo', 'exec')
            exec code in globals(), {}

        try:
            boo()
        except TypeError:
            msg = ("Issue #2 -- line monitor fails when exec is used"
                   " on code compiled from a string -- exists.")
            self.fail(msg)

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

    def check_records(self, template, recorder):
        expected = [line.format(self.filename) for line in template]
        records = self.get_records(recorder)
        self.assertEqual(records, expected)


if __name__ == '__main__':
    unittest.main()
