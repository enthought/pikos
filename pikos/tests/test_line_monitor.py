import StringIO
import unittest

from pikos.filters.api import OnValue
from pikos.monitors.api import LineMonitor
from pikos.recorders.api import TextStreamRecorder
from pikos.tests.compat import TestCase


class TestLineMonitor(TestCase):

    def setUp(self):
        self.filename = __file__.replace('.pyc', '.py')
        self.maxDiff = None
        self.stream = StringIO.StringIO()
        # we only care about the lines that are in this file and we filter
        # the others.
        self.recorder = TextStreamRecorder(
            text_stream=self.stream,
            filter_=OnValue('filename', self.filename))
        self.logger = LineMonitor(self.recorder)

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

        filename = self.filename

        # note the index depends on this file layout
        expected = [
            "index function lineNo line filename",
            "-----------------------------------",
            "0 gcd 28             while x > 0: {0}".format(filename),
            "1 gcd 29                 x, y = y % x, x {0}".format(filename),
            "2 gcd 28             while x > 0: {0}".format(filename),
            "3 gcd 29                 x, y = y % x, x {0}".format(filename),
            "4 gcd 28             while x > 0: {0}".format(filename),
            "5 gcd 30             return y {0}".format(filename)]

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

        filename = self.filename

        expected = [
            "index function lineNo line filename",
            "-----------------------------------",
            "0 gcd 61             return x if y == 0 else gcd(y, (x % y)) {0}".format(filename),
            "8 gcd 61             return x if y == 0 else gcd(y, (x % y)) {0}".format(filename),
            "16 gcd 61             return x if y == 0 else gcd(y, (x % y)) {0}".format(filename),
            "24 gcd 61             return x if y == 0 else gcd(y, (x % y)) {0}".format(filename),
            "32 gcd 61             return x if y == 0 else gcd(y, (x % y)) {0}".format(filename),
            "40 gcd 61             return x if y == 0 else gcd(y, (x % y)) {0}".format(filename)]

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
        filename = self.filename

        expected = [
            "index function lineNo line filename",
            "-----------------------------------",
            "0 fibonacci 90             x, y = 0, 1 {0}".format(filename),
            "1 fibonacci 91             for i in range(items): {0}".format(filename),
            "2 fibonacci 92                 yield x {0}".format(filename),
            "11 fibonacci 93                 x, y = y, x + y {0}".format(filename),
            "12 fibonacci 91             for i in range(items): {0}".format(filename),
            "13 fibonacci 92                 yield x {0}".format(filename),
            "22 fibonacci 93                 x, y = y, x + y {0}".format(filename),
            "23 fibonacci 91             for i in range(items): {0}".format(filename),
            "24 fibonacci 92                 yield x {0}".format(filename),
            "33 fibonacci 93                 x, y = y, x + y {0}".format(filename),
            "34 fibonacci 91             for i in range(items): {0}".format(filename),
            "35 fibonacci 92                 yield x {0}".format(filename),
            "44 fibonacci 93                 x, y = y, x + y {0}".format(filename),
            "45 fibonacci 91             for i in range(items): {0}".format(filename),
            "46 fibonacci 92                 yield x {0}".format(filename),
            "55 fibonacci 93                 x, y = y, x + y {0}".format(filename),
            "56 fibonacci 91             for i in range(items): {0}".format(filename),
            "57 fibonacci 92                 yield x {0}".format(filename),
            "66 fibonacci 93                 x, y = y, x + y {0}".format(filename),
            "67 fibonacci 91             for i in range(items): {0}".format(filename),
            "68 fibonacci 92                 yield x {0}".format(filename),
            "77 fibonacci 93                 x, y = y, x + y {0}".format(filename),
            "78 fibonacci 91             for i in range(items): {0}".format(filename),
            "79 fibonacci 92                 yield x {0}".format(filename),
            "88 fibonacci 93                 x, y = y, x + y {0}".format(filename),
            "89 fibonacci 91             for i in range(items): {0}".format(filename),
            "90 fibonacci 92                 yield x {0}".format(filename),
            "99 fibonacci 93                 x, y = y, x + y {0}".format(filename),
            "100 fibonacci 91             for i in range(items): {0}".format(filename),
            "101 fibonacci 92                 yield x {0}".format(filename),
            "110 fibonacci 93                 x, y = y, x + y {0}".format(filename),
            "111 fibonacci 91             for i in range(items): {0}".format(filename)]

        records = ''.join(self.stream.buflist).splitlines()
        self.assertEqual(records, expected)

    def test_issue2(self):
        """ Test for issue #2.

        The issues is reported in `https://github.com/sjagoe/pikos/issues/2`_

        """
        logger = self.logger

        FOO = """
def foo():
    a = []
    for i in range(20):
        a.append(i+sum(a))

foo()
"""

        @logger.attach
        def boo():
            code = compile(FOO, 'foo', 'exec')
            exec code in globals(), {}

        try:
            boo()
        except TypeError:
            msg = ("Issue #2 -- line monitor fails when exec is used"
                   " on code compiled from a string -- exists.")
            self.fail(msg)


if __name__ == '__main__':
    unittest.main()
