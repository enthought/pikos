import StringIO
import unittest

from pikos.filters.on_value import OnValue
from pikos.monitors.function_monitor import FunctionMonitor
from pikos.recorders.text_stream_recorder import TextStreamRecorder
from pikos.tests.compat import TestCase
from pikos.tests.monitoring_helper import MonitoringHelper


class TestFunctionMonitor(TestCase):

    def setUp(self):
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

    def test_function(self):
        result = self.helper.run_on_function()
        self.assertEqual(result, 3)
        template = [
            "index type function lineNo filename",
            "-----------------------------------",
            "3 call gcd 28 {0}",
            "4 return gcd 32 {0}"]
        self.check_records(template, self.stream)

    def test_recursive(self):
        result = self.helper.run_on_recursive_function()
        self.assertEqual(result, 1)
        template = [
            "index type function lineNo filename",
            "-----------------------------------",
            "3 call gcd 48 {0}",
            "11 call gcd 48 {0}",
            "19 call gcd 48 {0}",
            "27 call gcd 48 {0}",
            "35 call gcd 48 {0}",
            "43 call gcd 48 {0}",
            "44 return gcd 50 {0}",
            "52 return gcd 50 {0}",
            "60 return gcd 50 {0}",
            "68 return gcd 50 {0}",
            "76 return gcd 50 {0}",
            "84 return gcd 50 {0}"]
        self.check_records(template, self.stream)

    def test_generator(self):
        result = self.helper.run_on_generator()
        output = (0, 1, 1, 2, 3, 5, 8, 13, 21, 34)
        self.assertSequenceEqual(result, output)
        template = [
            "index type function lineNo filename",
            "-----------------------------------",
            "3 call fibonacci 63 {0}",
            "4 c_call range 66 {0}",
            "5 c_return range 66 {0}",
            "6 return fibonacci 67 {0}",
            "19 call fibonacci 67 {0}",
            "20 return fibonacci 67 {0}",
            "34 call fibonacci 67 {0}",
            "35 return fibonacci 67 {0}",
            "49 call fibonacci 67 {0}",
            "50 return fibonacci 67 {0}",
            "64 call fibonacci 67 {0}",
            "65 return fibonacci 67 {0}",
            "79 call fibonacci 67 {0}",
            "80 return fibonacci 67 {0}",
            "94 call fibonacci 67 {0}",
            "95 return fibonacci 67 {0}",
            "109 call fibonacci 67 {0}",
            "110 return fibonacci 67 {0}",
            "124 call fibonacci 67 {0}",
            "125 return fibonacci 67 {0}",
            "139 call fibonacci 67 {0}",
            "140 return fibonacci 67 {0}",
            "154 call fibonacci 67 {0}",
            "155 return fibonacci 68 {0}"]
        self.check_records(template, self.stream)

    def check_records(self, template, stream):
        expected = [line.format(self.filename) for line in template]
        records = ''.join(stream.buflist).splitlines()
        self.assertEqual(records, expected)


if __name__ == '__main__':
    unittest.main()
