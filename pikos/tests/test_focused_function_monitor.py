# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/test_focused_function_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
# ------------------------------------------------------------------------------
import StringIO
import unittest

from pikos.filters.on_value import OnValue
from pikos.monitors.focused_function_monitor import FocusedFunctionMonitor
from pikos.recorders.text_stream_recorder import TextStreamRecorder
from pikos.tests.compat import TestCase
from pikos.tests.focused_monitoring_helper import FocusedMonitoringHelper


class TestFocusedFunctionMonitor(TestCase):

    def setUp(self):
        self.maxDiff = None
        self.stream = StringIO.StringIO()

        def monitor_factory(functions=[]):
            return FocusedFunctionMonitor(
                functions=functions, recorder=self.recorder)

        self.helper = FocusedMonitoringHelper(monitor_factory)
        self.filename = self.helper.filename
        self.recorder = TextStreamRecorder(
            text_stream=self.stream,
            filter_=OnValue('filename', self.filename))

    def test_focus_on_function(self):
        result = self.helper.run_on_function()
        self.assertEqual(result, 3)
        template = [
            "index type function lineNo filename",
            "-----------------------------------",
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
        self.check_records(template, self.stream)
        self.assertEqual(self.helper.monitor._code_trackers, {})

    def test_focus_on_functions(self):
        result = self.helper.run_on_functions()
        self.assertEqual(result, 3)
        template = [
            "index type function lineNo filename",
            "-----------------------------------",
            "0 call gcd 63 {0}",
            "1 call internal 68 {0}",
            "2 return internal 69 {0}",
            "3 call internal 68 {0}",
            "4 return internal 69 {0}",
            "5 return gcd 66 {0}",
            "6 call foo 74 {0}",
            "7 call boo 71 {0}",
            "8 return boo 72 {0}",
            "9 call boo 71 {0}",
            "10 return boo 72 {0}",
            "11 return foo 76 {0}",
        ]
        self.check_records(template, self.stream)
        self.assertEqual(self.helper.monitor._code_trackers, {})

    def test_focus_on_recursive(self):
        result = self.helper.run_on_recursive_function()
        self.assertEqual(result, 3)
        template = [
            "index type function lineNo filename",
            "-----------------------------------",
            "0 call gcd 98 {0}",
            "1 call foo 105 {0}",
            "2 return foo 106 {0}",
            "3 call gcd 98 {0}",
            "4 call foo 105 {0}",
            "5 return foo 106 {0}",
            "6 return gcd 100 {0}",
            "7 return gcd 100 {0}"]
        self.check_records(template, self.stream)
        self.assertEqual(self.helper.monitor._code_trackers, {})

    def test_focus_on_decorated_function(self):
        result = self.helper.run_on_decorated()
        self.assertEqual(result, 3)
        template = [
            "index type function lineNo filename",
            "-----------------------------------",
            "0 call container 139 {0}",
            "1 call gcd 125 {0}",
            "2 call internal 130 {0}",
            "3 call boo 134 {0}",
            "4 return boo 135 {0}",
            "5 return internal 132 {0}",
            "6 call internal 130 {0}",
            "7 call boo 134 {0}",
            "8 return boo 135 {0}",
            "9 return internal 132 {0}",
            "10 return gcd 128 {0}",
            "11 call boo 134 {0}",
            "12 return boo 135 {0}",
            "13 return container 143 {0}"]
        self.check_records(template, self.stream)
        self.assertEqual(self.helper.monitor._code_trackers, {})

    def test_focus_on_decorated_recursive(self):
        result = self.helper.run_on_decorated_recursive()
        self.assertEqual(result, 3)
        template = [
            "index type function lineNo filename",
            "-----------------------------------",
            "0 call gcd 160 {0}",
            "1 call foo 155 {0}",
            "2 return foo 156 {0}",
            "10 call gcd 160 {0}",
            "11 call foo 155 {0}",
            "12 return foo 156 {0}",
            "13 return gcd 163 {0}",
            "21 return gcd 163 {0}"]
        self.check_records(template, self.stream)
        self.assertEqual(self.helper.monitor._code_trackers, {})

    def test_focus_on_function_using_tuples(self):
        recorder = TextStreamRecorder(
            text_stream=self.stream,
            filter_=lambda record: self.filename in record)

        def monitor_factory(functions=[]):
            return FocusedFunctionMonitor(
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
        self.check_records(template, self.stream)
        self.assertEqual(helper.monitor._code_trackers, {})

    def check_records(self, template, stream):
        expected = [line.format(self.filename) for line in template]
        records = ''.join(stream.buflist).splitlines()
        self.assertEqual(records, expected)


if __name__ == '__main__':
    unittest.main()
