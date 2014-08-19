# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: tests/test_c_function_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
# -----------------------------------------------------------------------------
import sys
import StringIO
import unittest

from pikos.filters.on_value import OnValue
from pikos.recorders.text_stream_recorder import TextStreamRecorder
from pikos.tests.compat import TestCase
from pikos.tests.monitoring_helper import MonitoringHelper


class TestCFunctionMonitor(TestCase):
    """ Test for the cython implementation of the FunctionMonitor
    """

    def setUp(self):
        try:
            from pikos.cymonitors.function_monitor import FunctionMonitor
        except ImportError:
            self.skipTest('Cython FunctionMonitor is not available')
        self.maxDiff = None
        self.stream = StringIO.StringIO()
        self.helper = MonitoringHelper()
        self.filename = self.helper.filename
        # we only care about the lines that are in this file and we filter
        # the others.
        self.recorder = TextStreamRecorder(
            text_stream=self.stream,
            filter_=OnValue('filename', self.filename))
        self.monitor = FunctionMonitor(self.recorder)
        self.helper.monitor = self.monitor

    def tearDown(self):
        sys.setprofile(None)

    def test_function(self):
        result = self.helper.run_on_function()
        self.assertEqual(result, 3)
        template = [
            u"index type function lineNo filename",
            u"-----------------------------------",
            u"0 call gcd 28 {0}",
            u"1 return gcd 32 {0}"]
        self.check_records(template, self.stream)

    def test_function_using_tuples(self):
        # tuple records are not compatible with the default OnValue filters.
        from pikos.cymonitors.function_monitor import FunctionMonitor
        recorder = TextStreamRecorder(
            text_stream=self.stream,
            filter_=lambda x: x[-1] == self.filename)
        monitor = FunctionMonitor(recorder, record_type=tuple)
        helper = MonitoringHelper(monitor)
        result = helper.run_on_function()
        self.assertEqual(result, 3)
        template = [
            "0 call gcd 28 {0}",
            "1 return gcd 32 {0}"]
        self.check_records(template, self.stream)

    def test_recursive(self):
        result = self.helper.run_on_recursive_function()
        self.assertEqual(result, 1)
        if sys.version_info[:2] == (2, 6):
            # Python 2.6 __enter__ is called through the CALL_FUNCTION
            # bytecode and thus the c __enter__ methods appears in the
            # function events while in 2.7 the behaviour has changed.
            template = [
                u"index type function lineNo filename",
                u"-----------------------------------",
                u"0 call gcd 48 {0}",
                u"6 call gcd 48 {0}",
                u"12 call gcd 48 {0}",
                u"18 call gcd 48 {0}",
                u"24 call gcd 48 {0}",
                u"30 call gcd 48 {0}",
                u"31 return gcd 50 {0}",
                u"35 return gcd 50 {0}",
                u"39 return gcd 50 {0}",
                u"43 return gcd 50 {0}",
                u"47 return gcd 50 {0}",
                u"51 return gcd 50 {0}"]
        else:
            template = [
                u"index type function lineNo filename",
                u"-----------------------------------",
                u"0 call gcd 48 {0}",
                u"4 call gcd 48 {0}",
                u"8 call gcd 48 {0}",
                u"12 call gcd 48 {0}",
                u"16 call gcd 48 {0}",
                u"20 call gcd 48 {0}",
                u"21 return gcd 50 {0}",
                u"25 return gcd 50 {0}",
                u"29 return gcd 50 {0}",
                u"33 return gcd 50 {0}",
                u"37 return gcd 50 {0}",
                u"41 return gcd 50 {0}"]
        self.check_records(template, self.stream)

    def test_generator(self):
        result = self.helper.run_on_generator()
        output = (0, 1, 1, 2, 3, 5, 8, 13, 21, 34)
        self.assertSequenceEqual(result, output)
        template = [
            u"index type function lineNo filename",
            u"-----------------------------------",
            u"0 call fibonacci 63 {0}",
            u"1 c_call range 66 {0}",
            u"2 c_return range 66 {0}",
            u"3 return fibonacci 67 {0}",
            u"7 call fibonacci 67 {0}",
            u"8 return fibonacci 67 {0}",
            u"13 call fibonacci 67 {0}",
            u"14 return fibonacci 67 {0}",
            u"19 call fibonacci 67 {0}",
            u"20 return fibonacci 67 {0}",
            u"25 call fibonacci 67 {0}",
            u"26 return fibonacci 67 {0}",
            u"31 call fibonacci 67 {0}",
            u"32 return fibonacci 67 {0}",
            u"37 call fibonacci 67 {0}",
            u"38 return fibonacci 67 {0}",
            u"43 call fibonacci 67 {0}",
            u"44 return fibonacci 67 {0}",
            u"49 call fibonacci 67 {0}",
            u"50 return fibonacci 67 {0}",
            u"55 call fibonacci 67 {0}",
            u"56 return fibonacci 67 {0}",
            u"61 call fibonacci 67 {0}",
            u"62 return fibonacci 68 {0}"]
        self.check_records(template, self.stream)

    def check_records(self, template, stream):
        expected = [line.format(self.filename) for line in template]
        records = ''.join(stream.buflist).splitlines()
        self.assertEqual(records, expected)


if __name__ == '__main__':
    unittest.main()
