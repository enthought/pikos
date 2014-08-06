import StringIO
import unittest

from pikos.filters.on_value import OnValue
from pikos.recorders.text_stream_recorder import TextStreamRecorder
from pikos.tests.compat import TestCase
from pikos.tests.monitoring_helper import MonitoringHelper


class TestCLineMonitor(TestCase):

    def setUp(self):
        try:
            from pikos.cymonitors.line_monitor import LineMonitor
        except ImportError:
            self.skipTest('Cython LineMonitor is not available')
        self.maxDiff = None
        self.stream = StringIO.StringIO()
        self.helper = MonitoringHelper()
        self.filename = self.helper.filename
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
            "1 gcd 30             while x > 0: {0}",
            "2 gcd 31                 x, y = y % x, x {0}",
            "3 gcd 30             while x > 0: {0}",
            "4 gcd 31                 x, y = y % x, x {0}",
            "5 gcd 30             while x > 0: {0}",
            "6 gcd 32             return y {0}"]

        self.check_records(template, self.stream)

    def test_recursive(self):
        result = self.helper.run_on_recursive_function()
        self.assertEqual(result, 1)

        template = [
            "index function lineNo line filename",
            "-----------------------------------",
            "1 gcd 50             return x if y == 0 else gcd(y, (x % y)) {0}",
            "7 gcd 50             return x if y == 0 else gcd(y, (x % y)) {0}",
            "13 gcd 50             return x if y == 0 else gcd(y, (x % y)) {0}",  # noqa
            "19 gcd 50             return x if y == 0 else gcd(y, (x % y)) {0}",  # noqa
            "25 gcd 50             return x if y == 0 else gcd(y, (x % y)) {0}",  # noqa
            "31 gcd 50             return x if y == 0 else gcd(y, (x % y)) {0}"]  # noqa

        self.check_records(template, self.stream)

    def test_generator(self):
        result = self.helper.run_on_generator()
        output = (0, 1, 1, 2, 3, 5, 8, 13, 21, 34)
        self.assertSequenceEqual(result, output)

        template = [
            "index function lineNo line filename",
            "-----------------------------------",
            "2 fibonacci 65             x, y = 0, 1 {0}",
            "3 fibonacci 66             for i in range(items): {0}",
            "4 fibonacci 67                 yield x {0}",
            "9 fibonacci 68                 x, y = y, x + y {0}",
            "10 fibonacci 66             for i in range(items): {0}",
            "11 fibonacci 67                 yield x {0}",
            "16 fibonacci 68                 x, y = y, x + y {0}",
            "17 fibonacci 66             for i in range(items): {0}",
            "18 fibonacci 67                 yield x {0}",
            "23 fibonacci 68                 x, y = y, x + y {0}",
            "24 fibonacci 66             for i in range(items): {0}",
            "25 fibonacci 67                 yield x {0}",
            "30 fibonacci 68                 x, y = y, x + y {0}",
            "31 fibonacci 66             for i in range(items): {0}",
            "32 fibonacci 67                 yield x {0}",
            "37 fibonacci 68                 x, y = y, x + y {0}",
            "38 fibonacci 66             for i in range(items): {0}",
            "39 fibonacci 67                 yield x {0}",
            "44 fibonacci 68                 x, y = y, x + y {0}",
            "45 fibonacci 66             for i in range(items): {0}",
            "46 fibonacci 67                 yield x {0}",
            "51 fibonacci 68                 x, y = y, x + y {0}",
            "52 fibonacci 66             for i in range(items): {0}",
            "53 fibonacci 67                 yield x {0}",
            "58 fibonacci 68                 x, y = y, x + y {0}",
            "59 fibonacci 66             for i in range(items): {0}",
            "60 fibonacci 67                 yield x {0}",
            "65 fibonacci 68                 x, y = y, x + y {0}",
            "66 fibonacci 66             for i in range(items): {0}",
            "67 fibonacci 67                 yield x {0}",
            "72 fibonacci 68                 x, y = y, x + y {0}",
            "73 fibonacci 66             for i in range(items): {0}"]

        self.check_records(template, self.stream)

    def test_function_using_tuples(self):
        from pikos.cymonitors.line_monitor import LineMonitor
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
            "1 gcd 30             while x > 0: {0}",
            "2 gcd 31                 x, y = y % x, x {0}",
            "3 gcd 30             while x > 0: {0}",
            "4 gcd 31                 x, y = y % x, x {0}",
            "5 gcd 30             while x > 0: {0}",
            "6 gcd 32             return y {0}"]
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
