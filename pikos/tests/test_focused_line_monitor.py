# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/test_focused_line_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012-2014, Enthought, Inc.
#  All rights reserved.
# -----------------------------------------------------------------------------
import StringIO
import unittest

from pikos.monitors.focused_line_monitor import FocusedLineMonitor
from pikos.recorders.text_stream_recorder import TextStreamRecorder
from pikos.tests.compat import TestCase
from pikos.tests.focused_monitoring_helper import FocusedMonitoringHelper


class TestFocusedLineMonitor(TestCase):

    def setUp(self):
        self.maxDiff = None
        self.stream = StringIO.StringIO()

        def monitor_factory(functions=[]):
            return FocusedLineMonitor(
                functions=functions, recorder=self.recorder)

        self.helper = FocusedMonitoringHelper(monitor_factory)
        self.filename = self.helper.filename
        self.recorder = TextStreamRecorder(
            text_stream=self.stream)

    def test_focus_on_function(self):
        result = self.helper.run_on_function()
        self.assertEqual(result, 3)
        template = [
            "index function lineNo line filename",
            "-----------------------------------",
            "0 gcd 34             while x > 0: {0}",
            "1 gcd 35                 x, y = internal(x, y) {0}",
            "2 gcd 34             while x > 0: {0}",
            "3 gcd 35                 x, y = internal(x, y) {0}",
            "4 gcd 34             while x > 0: {0}",
            "5 gcd 36             return y {0}"]
        self.check_records(template, self.stream)

    def test_focus_on_functions(self):
        result = self.helper.run_on_functions()
        self.assertEqual(result, 3)
        template = [
            "index function lineNo line filename",
            "-----------------------------------",
            "0 gcd 64             while x > 0: {0}",
            "1 gcd 65                 x, y = internal(x, y) {0}",
            "2 gcd 64             while x > 0: {0}",
            "3 gcd 65                 x, y = internal(x, y) {0}",
            "4 gcd 64             while x > 0: {0}",
            "5 gcd 66             return y {0}",
            "6 foo 75             boo() {0}",
            "7 foo 76             boo() {0}"]
        self.check_records(template, self.stream)

    def test_focus_on_recursive(self):
        result = self.helper.run_on_recursive_function()
        self.assertEqual(result, 3)
        template = [
            "index function lineNo line filename",
            "-----------------------------------",
            "0 gcd 99             foo() {0}",
            "1 gcd 100             return x if y == 0 else gcd(y, (x % y)) {0}",  # noqa
            "2 gcd 99             foo() {0}",
            "3 gcd 100             return x if y == 0 else gcd(y, (x % y)) {0}"]  # noqa
        self.check_records(template, self.stream)

    def test_focus_on_decorated_function(self):
        result = self.helper.run_on_decorated()
        self.assertEqual(result, 3)
        template = [
            "index function lineNo line filename",
            "-----------------------------------",
            "0 container 141             result = gcd(x, y) {0}",
            "1 gcd 126             while x > 0: {0}",
            "2 gcd 127                 x, y = internal(x, y) {0}",
            "3 gcd 126             while x > 0: {0}",
            "4 gcd 127                 x, y = internal(x, y) {0}",
            "5 gcd 126             while x > 0: {0}",
            "6 gcd 128             return y {0}",
            "7 container 142             boo() {0}",
            "8 container 143             return result {0}"]
        self.check_records(template, self.stream)

    def test_focus_on_decorated_recursive_function(self):
        result = self.helper.run_on_decorated_recursive()
        self.assertEqual(result, 3)
        template = [
            "index function lineNo line filename",
            "-----------------------------------",
            "0 gcd 162             foo() {0}",
            "1 gcd 163             return x if y == 0 else gcd(y, (x % y)) {0}",  # noqa
            "2 gcd 162             foo() {0}",
            "3 gcd 163             return x if y == 0 else gcd(y, (x % y)) {0}"]  # noqa
        self.check_records(template, self.stream)

    def test_focus_on_function_with_tuple(self):
        recorder = TextStreamRecorder(
            text_stream=self.stream,
            filter_=lambda record: self.filename in record)

        def monitor_factory(functions=[]):
            return FocusedLineMonitor(
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
        self.check_records(template, self.stream)

    def check_records(self, template, stream):
        template = [line.format(self.filename) for line in template]
        records = ''.join(stream.buflist).splitlines()
        self.assertEqual(records, template)


if __name__ == '__main__':
    unittest.main()
