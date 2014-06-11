# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: tests/test_function_memory_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
# -----------------------------------------------------------------------------
import unittest

from pikos.recorders.list_recorder import ListRecorder
from pikos.filters.on_value import OnValue
from pikos.tests.test_assistant import TestAssistant
from pikos.tests.compat import TestCase
from pikos.tests.monitoring_helper import MonitoringHelper


class TestFunctionMemoryMonitor(TestCase, TestAssistant):

    def setUp(self):
        self.check_for_psutils()
        from pikos.monitors.function_memory_monitor import (
            FunctionMemoryMonitor)
        self.monitor_type = FunctionMemoryMonitor
        self.maxDiff = None
        self.helper = MonitoringHelper()
        self.filename = self.helper.filename
        self.recorder = ListRecorder(
            filter_=OnValue('filename', self.filename))
        self.monitor = self.monitor_type(self.recorder)
        self.helper.monitor = self.monitor

    def test_function(self):
        result = self.helper.run_on_function()
        self.assertEqual(result, 3)
        template = [
            "3 call gcd 27 {0}",
            "4 return gcd 31 {0}"]
        self.check_records(template, self.recorder)

    def test_recursive(self):
        result = self.helper.run_on_recursive_function()
        self.assertEqual(result, 3)
        template = [
            "3 call gcd 47 {0}",
            "11 call gcd 47 {0}",
            "19 call gcd 47 {0}",
            "27 call gcd 47 {0}",
            "35 call gcd 47 {0}",
            "43 call gcd 47 {0}",
            "44 return gcd 49 {0}",
            "52 return gcd 49 {0}",
            "60 return gcd 49 {0}",
            "68 return gcd 49 {0}",
            "76 return gcd 49 {0}",
            "84 return gcd 49 {0}"]
        self.check_records(template, self.recorder)

    def test_generator(self):
        result = self.helper.run_on_generator()
        output = (0, 1, 1, 2, 3, 5, 8, 13, 21, 34)
        self.assertSequenceEqual(result, output)
        template = [
            "3 call fibonacci 62 {0}",
            "4 c_call range 65 {0}",
            "5 c_return range 65 {0}",
            "6 return fibonacci 66 {0}",
            "19 call fibonacci 66 {0}",
            "20 return fibonacci 66 {0}",
            "34 call fibonacci 66 {0}",
            "35 return fibonacci 66 {0}",
            "49 call fibonacci 66 {0}",
            "50 return fibonacci 66 {0}",
            "64 call fibonacci 66 {0}",
            "65 return fibonacci 66 {0}",
            "79 call fibonacci 66 {0}",
            "80 return fibonacci 66 {0}",
            "94 call fibonacci 66 {0}",
            "95 return fibonacci 66 {0}",
            "109 call fibonacci 66 {0}",
            "110 return fibonacci 66 {0}",
            "124 call fibonacci 66 {0}",
            "125 return fibonacci 66 {0}",
            "139 call fibonacci 66 {0}",
            "140 return fibonacci 66 {0}",
            "154 call fibonacci 66 {0}",
            "155 return fibonacci 67 {0}"]
        self.check_records(template, self.recorder)

    def test_function_using_tuples(self):
        # tuple records are not compatible with the default OnValue filters.
        recorder = ListRecorder(filter_=lambda x: x[-1] == self.filename)
        monitor = self.monitor_type(recorder, record_type=tuple)
        helper = MonitoringHelper(monitor)
        result = helper.run_on_function()
        self.assertEqual(result, 3)
        template = [
            "3 call gcd 27 {0}",
            "4 return gcd 31 {0}"]
        self.check_records(template, recorder)

    def check_for_psutils(self):
        try:
            import psutil  # noqa
        except ImportError:
            self.skipTest('Could not import psutils, skipping test.')

    def check_records(self, template, recorder):
        expected = [line.format(self.filename) for line in template]
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


if __name__ == '__main__':
    unittest.main()
