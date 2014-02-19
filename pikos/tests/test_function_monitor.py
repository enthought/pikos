import StringIO
import unittest

from pikos.filters.on_value import OnValue
from pikos.monitors.function_monitor import FunctionMonitor
from pikos.recorders.text_stream_recorder import TextStreamRecorder
from pikos.tests.compat import TestCase


class TestFunctionMonitor(TestCase):

    def setUp(self):
        self.filename = __file__.replace('.pyc', '.py')
        self.maxDiff = None
        self.stream = StringIO.StringIO()
        # we only care about the lines that are in this file and we filter
        # the others.
        self.recorder = TextStreamRecorder(
            text_stream=self.stream,
            filter_=OnValue('filename', self.filename))
        self.logger = FunctionMonitor(self.recorder)

    def test_function(self):
        logger = self.logger

        @logger.attach
        def gcd(x, y):
            while x > 0:
                x, y = y % x, x
            return y

        def boo():
            pass

        boo()
        result = gcd(12, 3)
        boo()
        self.assertEqual(result, 3)
        expected = [
            "index type function lineNo filename",
            "-----------------------------------",
            "3 call gcd 26 {0}".format(self.filename),
            "4 return gcd 30 {0}".format(self.filename)]
        records = ''.join(self.stream.buflist).splitlines()
        self.assertEqual(records, expected)

    def test_recursive(self):
        logger = self.logger

        @logger.attach
        def gcd(x, y):
            return x if y == 0 else gcd(y, (x % y))

        def boo():
            return gcd(7, 12)

        result = boo()
        self.assertEqual(result, 1)
        expected = [
            "index type function lineNo filename",
            "-----------------------------------",
            "3 call gcd 50 {0}".format(self.filename),
            "11 call gcd 50 {0}".format(self.filename),
            "19 call gcd 50 {0}".format(self.filename),
            "27 call gcd 50 {0}".format(self.filename),
            "35 call gcd 50 {0}".format(self.filename),
            "43 call gcd 50 {0}".format(self.filename),
            "44 return gcd 52 {0}".format(self.filename),
            "52 return gcd 52 {0}".format(self.filename),
            "60 return gcd 52 {0}".format(self.filename),
            "68 return gcd 52 {0}".format(self.filename),
            "76 return gcd 52 {0}".format(self.filename),
            "84 return gcd 52 {0}".format(self.filename)]
        records = ''.join(self.stream.buflist).splitlines()
        self.assertEqual(records, expected)

    def test_generator(self):
        logger = self.logger
        output = (0, 1, 1, 2, 3, 5, 8, 13, 21, 34)

        @logger.attach
        def fibonacci(items):
            x, y = 0, 1
            for i in range(items):
                yield x
                x, y = y, x + y

        def boo():
            pass

        boo()
        result = [value for value in fibonacci(10)]
        boo()
        self.assertSequenceEqual(result, output)
        expected = [
            "index type function lineNo filename",
            "-----------------------------------",
            "3 call fibonacci 81 {0}".format(self.filename),
            "4 c_call range 84 {0}".format(self.filename),
            "5 c_return range 84 {0}".format(self.filename),
            "6 return fibonacci 85 {0}".format(self.filename),
            "19 call fibonacci 85 {0}".format(self.filename),
            "20 return fibonacci 85 {0}".format(self.filename),
            "34 call fibonacci 85 {0}".format(self.filename),
            "35 return fibonacci 85 {0}".format(self.filename),
            "49 call fibonacci 85 {0}".format(self.filename),
            "50 return fibonacci 85 {0}".format(self.filename),
            "64 call fibonacci 85 {0}".format(self.filename),
            "65 return fibonacci 85 {0}".format(self.filename),
            "79 call fibonacci 85 {0}".format(self.filename),
            "80 return fibonacci 85 {0}".format(self.filename),
            "94 call fibonacci 85 {0}".format(self.filename),
            "95 return fibonacci 85 {0}".format(self.filename),
            "109 call fibonacci 85 {0}".format(self.filename),
            "110 return fibonacci 85 {0}".format(self.filename),
            "124 call fibonacci 85 {0}".format(self.filename),
            "125 return fibonacci 85 {0}".format(self.filename),
            "139 call fibonacci 85 {0}".format(self.filename),
            "140 return fibonacci 85 {0}".format(self.filename),
            "154 call fibonacci 85 {0}".format(self.filename),
            "155 return fibonacci 86 {0}".format(self.filename)]
        records = ''.join(self.stream.buflist).splitlines()
        self.assertEqual(records, expected)


if __name__ == '__main__':
    unittest.main()
