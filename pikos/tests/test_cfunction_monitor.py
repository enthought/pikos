import StringIO
import unittest

from pikos.filters.on_value import OnValue
from pikos.recorders.text_stream_recorder import TextStreamRecorder
from pikos.tests.compat import TestCase


class TestFunctionMonitor(TestCase):

    def setUp(self):
        try:
            from pikos.cmonitors.cfunction_monitor import CFunctionMonitor
        except ImportError:
            self.skipTest('CFunctionMonitor is not available')
        self.filename = __file__.replace('.pyc', '.py')
        self.maxDiff = None
        self.stream = StringIO.StringIO()
        # we only care about the lines that are in this file and we filter
        # the others.
        self.recorder = TextStreamRecorder(
            text_stream=self.stream,
            filter_=OnValue('filename', self.filename))
        self.logger = CFunctionMonitor(self.recorder)

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
            "0 call gcd 26 {0}".format(self.filename),
            "1 return gcd 30 {0}".format(self.filename)]
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
            "0 call gcd 50 {0}".format(self.filename),
            "4 call gcd 50 {0}".format(self.filename),
            "8 call gcd 50 {0}".format(self.filename),
            "12 call gcd 50 {0}".format(self.filename),
            "16 call gcd 50 {0}".format(self.filename),
            "20 call gcd 50 {0}".format(self.filename),
            "21 return gcd 52 {0}".format(self.filename),
            "25 return gcd 52 {0}".format(self.filename),
            "29 return gcd 52 {0}".format(self.filename),
            "33 return gcd 52 {0}".format(self.filename),
            "37 return gcd 52 {0}".format(self.filename),
            "41 return gcd 52 {0}".format(self.filename)]
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
            "0 call fibonacci 81 {0}".format(self.filename),
            "1 c_call range 84 {0}".format(self.filename),
            "2 c_return range 84 {0}".format(self.filename),
            "3 return fibonacci 85 {0}".format(self.filename),
            "7 call fibonacci 85 {0}".format(self.filename),
            "8 return fibonacci 85 {0}".format(self.filename),
            "13 call fibonacci 85 {0}".format(self.filename),
            "14 return fibonacci 85 {0}".format(self.filename),
            "19 call fibonacci 85 {0}".format(self.filename),
            "20 return fibonacci 85 {0}".format(self.filename),
            "25 call fibonacci 85 {0}".format(self.filename),
            "26 return fibonacci 85 {0}".format(self.filename),
            "31 call fibonacci 85 {0}".format(self.filename),
            "32 return fibonacci 85 {0}".format(self.filename),
            "37 call fibonacci 85 {0}".format(self.filename),
            "38 return fibonacci 85 {0}".format(self.filename),
            "43 call fibonacci 85 {0}".format(self.filename),
            "44 return fibonacci 85 {0}".format(self.filename),
            "49 call fibonacci 85 {0}".format(self.filename),
            "50 return fibonacci 85 {0}".format(self.filename),
            "55 call fibonacci 85 {0}".format(self.filename),
            "56 return fibonacci 85 {0}".format(self.filename),
            "61 call fibonacci 85 {0}".format(self.filename),
            "62 return fibonacci 86 {0}".format(self.filename)]
        records = ''.join(self.stream.buflist).splitlines()
        self.assertEqual(records, expected)


if __name__ == '__main__':
    unittest.main()
