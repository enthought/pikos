# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/test_focused_line_memory_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
# -----------------------------------------------------------------------------
import StringIO
import unittest

from pikos.recorders.list_recorder import ListRecorder
from pikos.tests.compat import TestCase
from pikos.tests.focused_monitoring_helper import FocusedMonitoringHelper


class TestFocusedLineMemoryMonitor(TestCase):

    def setUp(self):
        self.check_for_psutils()
        from pikos.monitors.focused_line_memory_monitor import (
            FocusedLineMemoryMonitor)

        self.maxDiff = None
        self.stream = StringIO.StringIO()

        def monitor_factory(functions=[]):
            return FocusedLineMemoryMonitor(
                functions=functions, recorder=self.recorder)

        self.helper = FocusedMonitoringHelper(monitor_factory)
        self.filename = self.helper.filename
        self.recorder = ListRecorder()

    def test_focus_on_function(self):
        result = self.helper.run_on_function()
        self.assertEqual(result, 3)
        template = [
            "0 gcd 34             while x > 0: {0}",
            "1 gcd 35                 x, y = internal(x, y) {0}",
            "2 gcd 34             while x > 0: {0}",
            "3 gcd 35                 x, y = internal(x, y) {0}",
            "4 gcd 34             while x > 0: {0}",
            "5 gcd 36             return y {0}"]
        self.check_records(template, self.recorder)

    def test_focus_on_functions(self):
        result = self.helper.run_on_functions()
        self.assertEqual(result, 3)
        template = [
            "0 gcd 63             while x > 0: {0}",
            "1 gcd 64                 x, y = internal(x, y) {0}",
            "2 gcd 63             while x > 0: {0}",
            "3 gcd 64                 x, y = internal(x, y) {0}",
            "4 gcd 63             while x > 0: {0}",
            "5 gcd 65             return y {0}",
            "6 foo 74             boo() {0}",
            "7 foo 75             boo() {0}"]
        self.check_records(template, self.recorder)

    def test_focus_on_recursive(self):
        result = self.helper.run_on_recursive_function()
        self.assertEqual(result, 3)
        template = [
            "0 gcd 97             foo() {0}",
            "1 gcd 98             return x if y == 0 else gcd(y, (x % y)) {0}",  # noqa
            "2 gcd 97             foo() {0}",
            "3 gcd 98             return x if y == 0 else gcd(y, (x % y)) {0}"]  # noqa
        self.check_records(template, self.recorder)

    def test_focus_on_decorated_recursive_function(self):
        result = self.helper.run_on_decorated_recursive()
        self.assertEqual(result, 3)
        template = [
            "0 gcd 159             foo() {0}",
            "1 gcd 160             return x if y == 0 else gcd(y, (x % y)) {0}",  # noqa
            "2 gcd 159             foo() {0}",
            "3 gcd 160             return x if y == 0 else gcd(y, (x % y)) {0}"]  # noqa
        self.check_records(template, self.recorder)

    def test_focus_on_decorated_function(self):
        result = self.helper.run_on_decorated()
        self.assertEqual(result, 3)
        template = [
            "0 container 139             result = gcd(x, y) {0}",
            "1 gcd 124             while x > 0: {0}",
            "2 gcd 125                 x, y = internal(x, y) {0}",
            "3 gcd 124             while x > 0: {0}",
            "4 gcd 125                 x, y = internal(x, y) {0}",
            "5 gcd 124             while x > 0: {0}",
            "6 gcd 126             return y {0}",
            "7 container 140             boo() {0}",
            "8 container 141             return result {0}"]
        self.check_records(template, self.recorder)

    def test_focus_on_function_using_tuples(self):
        recorder = ListRecorder()

        def monitor_factory(functions=[]):
            from pikos.monitors.focused_line_memory_monitor import (
                FocusedLineMemoryMonitor)
            return FocusedLineMemoryMonitor(
                functions=functions,
                recorder=recorder,
                record_type=tuple)

        helper = FocusedMonitoringHelper(monitor_factory)
        result = helper.run_on_function()
        self.assertEqual(result, 3)
        template = [
            "0 gcd 34             while x > 0: {0}",
            "1 gcd 35                 x, y = internal(x, y) {0}",
            "2 gcd 34             while x > 0: {0}",
            "3 gcd 35                 x, y = internal(x, y) {0}",
            "4 gcd 34             while x > 0: {0}",
            "5 gcd 36             return y {0}"]
        self.check_records(template, recorder)

    def get_records(self, recorder):
        """ Remove the memory related fields.
        """
        records = []
        for record in recorder.records:
            filtered = record[:3] + record[5:]
            records.append(' '.join([str(item) for item in filtered]))
        return records

    def check_for_psutils(self):
        try:
            import psutil  # noqa
        except ImportError:
            self.skipTest('Could not import psutils, skipping test.')

    def check_records(self, template, recorder):
        expected = [line.format(self.filename) for line in template]
        records = self.get_records(recorder)
        self.assertEqual(records, expected)


if __name__ == '__main__':
    unittest.main()
