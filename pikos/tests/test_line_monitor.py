import StringIO
import unittest

from pikos.filters.on_value import OnValue
from pikos.monitors.line_monitor import LineMonitor
from pikos.recorders.text_stream_recorder import TextStreamRecorder
from pikos.tests.compat import TestCase
from pikos.tests.monitoring_helper import MonitoringHelper


class TestLineMonitor(TestCase):

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
        self.monitor = LineMonitor(self.recorder)
        self.helper.monitor = self.monitor

    def test_function(self):
        result = self.helper.run_on_function()
        self.assertEqual(result, 3)

        template = [
            "index function lineNo line filename",
            "-----------------------------------",
            "0 gcd 29             while x > 0: {0}",
            "1 gcd 30                 x, y = y % x, x {0}",
            "2 gcd 29             while x > 0: {0}",
            "3 gcd 30                 x, y = y % x, x {0}",
            "4 gcd 29             while x > 0: {0}",
            "5 gcd 31             return y {0}"]

        self.check_records(template, self.stream)

    def test_recursive(self):
        result = self.helper.run_on_recursive_function()
        self.assertEqual(result, 1)

        filename = self.filename

        template = [
            "index function lineNo line filename",
            "-----------------------------------",
            "0 gcd 49             return x if y == 0 else gcd(y, (x % y)) {0}",
            "8 gcd 49             return x if y == 0 else gcd(y, (x % y)) {0}",
            "16 gcd 49             return x if y == 0 else gcd(y, (x % y)) {0}",
            "24 gcd 49             return x if y == 0 else gcd(y, (x % y)) {0}",
            "32 gcd 49             return x if y == 0 else gcd(y, (x % y)) {0}",
            "40 gcd 49             return x if y == 0 else gcd(y, (x % y)) {0}"]

        self.check_records(template, self.stream)

    def test_generator(self):
        result = self.helper.run_on_generator()
        output = (0, 1, 1, 2, 3, 5, 8, 13, 21, 34)
        self.assertSequenceEqual(result, output)

        template = [
            "index function lineNo line filename",
            "-----------------------------------",
            "0 fibonacci 64             x, y = 0, 1 {0}",
            "1 fibonacci 65             for i in range(items): {0}",
            "2 fibonacci 66                 yield x {0}",
            "11 fibonacci 67                 x, y = y, x + y {0}",
            "12 fibonacci 65             for i in range(items): {0}",
            "13 fibonacci 66                 yield x {0}",
            "22 fibonacci 67                 x, y = y, x + y {0}",
            "23 fibonacci 65             for i in range(items): {0}",
            "24 fibonacci 66                 yield x {0}",
            "33 fibonacci 67                 x, y = y, x + y {0}",
            "34 fibonacci 65             for i in range(items): {0}",
            "35 fibonacci 66                 yield x {0}",
            "44 fibonacci 67                 x, y = y, x + y {0}",
            "45 fibonacci 65             for i in range(items): {0}",
            "46 fibonacci 66                 yield x {0}",
            "55 fibonacci 67                 x, y = y, x + y {0}",
            "56 fibonacci 65             for i in range(items): {0}",
            "57 fibonacci 66                 yield x {0}",
            "66 fibonacci 67                 x, y = y, x + y {0}",
            "67 fibonacci 65             for i in range(items): {0}",
            "68 fibonacci 66                 yield x {0}",
            "77 fibonacci 67                 x, y = y, x + y {0}",
            "78 fibonacci 65             for i in range(items): {0}",
            "79 fibonacci 66                 yield x {0}",
            "88 fibonacci 67                 x, y = y, x + y {0}",
            "89 fibonacci 65             for i in range(items): {0}",
            "90 fibonacci 66                 yield x {0}",
            "99 fibonacci 67                 x, y = y, x + y {0}",
            "100 fibonacci 65             for i in range(items): {0}",
            "101 fibonacci 66                 yield x {0}",
            "110 fibonacci 67                 x, y = y, x + y {0}",
            "111 fibonacci 65             for i in range(items): {0}"]

        self.check_records(template, self.stream)

    def test_function_using_tuples(self):
        filename = self.filename
        # tuple records are not compatible with the default OnValue filters.
        recorder = TextStreamRecorder(
            text_stream=self.stream,
            filter_=lambda x: x[-1] == filename)
        monitor = LineMonitor(recorder, record_type=tuple)
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
        self.check_records(template, self.stream)

    def test_issue2(self):
        """ Test for issue #2.

        The issues is reported in `https://github.com/sjagoe/pikos/issues/2`_

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

    def check_records(self, template, stream):
        expected = [line.format(self.filename) for line in template]
        records = ''.join(stream.buflist).splitlines()
        self.assertEqual(records, expected)

if __name__ == '__main__':
    unittest.main()
