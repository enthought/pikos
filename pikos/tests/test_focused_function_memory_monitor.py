# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/test_focused_function_memory_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
# -----------------------------------------------------------------------------
import sys
import unittest

from pikos.filters.on_value import OnValue
from pikos.recorders.list_recorder import ListRecorder
from pikos.tests.compat import TestCase
from pikos.tests.focused_monitoring_helper import FocusedMonitoringHelper


class TestFocusedFunctionMemoryMonitor(TestCase):

    def setUp(self):
        self.check_for_psutils()
        self.maxDiff = None

        # local import to avoid errors when the optional depedency psutils is
        # not available
        from pikos.monitors.focused_function_memory_monitor import (
            FocusedFunctionMemoryMonitor)

        def monitor_factory(functions=[]):
            return FocusedFunctionMemoryMonitor(
                functions=functions, recorder=self.recorder)

        self.helper = FocusedMonitoringHelper(monitor_factory)
        self.filename = self.helper.filename
        self.recorder = ListRecorder(
            filter_=OnValue('filename', self.filename))

    def tearDown(self):
        sys.setprofile(None)

    def test_focus_on_function(self):
        result = self.helper.run_on_function()
        self.assertEqual(result, 3)
        template = [
            "0 call gcd 33 {0}",
            "1 call internal 40 {0}",
            "2 call boo 44 {0}",
            "3 return boo 45 {0}",
            "4 return internal 42 {0}",
            "5 call internal 40 {0}",
            "6 call boo 44 {0}",
            "7 return boo 45 {0}",
            "8 return internal 42 {0}",
            "9 return gcd 36 {0}"]
        self.check_records(template, self.recorder)
        self.assertEqual(self.helper.monitor._code_trackers, {})

    def test_focus_on_functions(self):
        result = self.helper.run_on_functions()
        self.assertEqual(result, 3)
        template = [
            "0 call gcd 62 {0}",
            "1 call internal 67 {0}",
            "2 return internal 68 {0}",
            "3 call internal 67 {0}",
            "4 return internal 68 {0}",
            "5 return gcd 65 {0}",
            "6 call foo 73 {0}",
            "7 call boo 70 {0}",
            "8 return boo 71 {0}",
            "9 call boo 70 {0}",
            "10 return boo 71 {0}",
            "11 return foo 75 {0}",
        ]
        self.check_records(template, self.recorder)
        self.assertEqual(self.helper.monitor._code_trackers, {})

    def test_focus_on_recursive(self):
        result = self.helper.run_on_recursive_function()
        self.assertEqual(result, 3)
        template = [
            "0 call gcd 96 {0}",
            "1 call foo 103 {0}",
            "2 return foo 104 {0}",
            "3 call gcd 96 {0}",
            "4 call foo 103 {0}",
            "5 return foo 104 {0}",
            "6 return gcd 98 {0}",
            "7 return gcd 98 {0}"]
        self.check_records(template, self.recorder)
        self.assertEqual(self.helper.monitor._code_trackers, {})

    def test_focus_on_decorated_function(self):
        result = self.helper.run_on_decorated()
        self.assertEqual(result, 3)
        template = [
            "0 call container 137 {0}",
            "1 call gcd 123 {0}",
            "2 call internal 128 {0}",
            "3 call boo 132 {0}",
            "4 return boo 133 {0}",
            "5 return internal 130 {0}",
            "6 call internal 128 {0}",
            "7 call boo 132 {0}",
            "8 return boo 133 {0}",
            "9 return internal 130 {0}",
            "10 return gcd 126 {0}",
            "11 call boo 132 {0}",
            "12 return boo 133 {0}",
            "13 return container 141 {0}"]
        self.check_records(template, self.recorder)
        self.assertEqual(self.helper.monitor._code_trackers, {})

    def test_focus_on_decorated_recursive(self):
        result = self.helper.run_on_decorated_recursive()
        self.assertEqual(result, 3)
        template = [
            "0 call gcd 157 {0}",
            "1 call foo 152 {0}",
            "2 return foo 153 {0}",
            "10 call gcd 157 {0}",
            "11 call foo 152 {0}",
            "12 return foo 153 {0}",
            "13 return gcd 160 {0}",
            "21 return gcd 160 {0}"]
        self.check_records(template, self.recorder)
        self.assertEqual(self.helper.monitor._code_trackers, {})

    def test_focus_on_function_using_tuples(self):

        # local import to avoid errors when the optional depedency psutils is
        # not available
        from pikos.monitors.focused_function_memory_monitor import (
            FocusedFunctionMemoryMonitor)

        recorder = ListRecorder(
            filter_=lambda record: self.filename in record)

        def monitor_factory(functions=[]):
            return FocusedFunctionMemoryMonitor(
                functions=functions,
                recorder=recorder,
                record_type=tuple)

        helper = FocusedMonitoringHelper(monitor_factory)
        result = helper.run_on_function()
        self.assertEqual(result, 3)
        template = [
            "0 call gcd 33 {0}",
            "1 call internal 40 {0}",
            "2 call boo 44 {0}",
            "3 return boo 45 {0}",
            "4 return internal 42 {0}",
            "5 call internal 40 {0}",
            "6 call boo 44 {0}",
            "7 return boo 45 {0}",
            "8 return internal 42 {0}",
            "9 return gcd 36 {0}"]
        self.check_records(template, recorder)
        self.assertEqual(helper.monitor._code_trackers, {})

    def get_records(self, recorder):
        """ Remove the memory related fields.
        """
        records = []
        for record in recorder.records:
            filtered = record[:3] + record[5:]
            records.append(' '.join([str(item) for item in filtered]))
        return records

    def check_records(self, template, recorder):
        expected = [line.format(self.filename) for line in template]
        records = self.get_records(recorder)
        self.assertEqual(records, expected)

    def check_for_psutils(self):
        try:
            import psutil
            psutil
        except ImportError:
            self.skipTest('Could not import psutils, skipping test.')


if __name__ == '__main__':
    unittest.main()
