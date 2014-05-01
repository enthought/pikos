import StringIO
import unittest

from pikos.filters.on_value import OnValue
from pikos.monitors.line_monitor import LineMonitor
from pikos.recorders.text_stream_recorder import TextStreamRecorder
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
            "0 gcd 61             return x if y == 0 else gcd(y, (x % y)) {0}".format(filename),  # noqa
            "8 gcd 61             return x if y == 0 else gcd(y, (x % y)) {0}".format(filename),  # noqa
            "16 gcd 61             return x if y == 0 else gcd(y, (x % y)) {0}".format(filename),  # noqa
            "24 gcd 61             return x if y == 0 else gcd(y, (x % y)) {0}".format(filename),  # noqa
            "32 gcd 61             return x if y == 0 else gcd(y, (x % y)) {0}".format(filename),  # noqa
            "40 gcd 61             return x if y == 0 else gcd(y, (x % y)) {0}".format(filename)]  # noqa

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
            "1 fibonacci 91             for i in range(items): {0}".format(filename),  # noqa
            "2 fibonacci 92                 yield x {0}".format(filename),  # noqa
            "11 fibonacci 93                 x, y = y, x + y {0}".format(filename),  # noqa
            "12 fibonacci 91             for i in range(items): {0}".format(filename),  # noqa
            "13 fibonacci 92                 yield x {0}".format(filename),  # noqa
            "22 fibonacci 93                 x, y = y, x + y {0}".format(filename),  # noqa
            "23 fibonacci 91             for i in range(items): {0}".format(filename),  # noqa
            "24 fibonacci 92                 yield x {0}".format(filename),  # noqa
            "33 fibonacci 93                 x, y = y, x + y {0}".format(filename),  # noqa
            "34 fibonacci 91             for i in range(items): {0}".format(filename),  # noqa
            "35 fibonacci 92                 yield x {0}".format(filename),  # noqa
            "44 fibonacci 93                 x, y = y, x + y {0}".format(filename),  # noqa
            "45 fibonacci 91             for i in range(items): {0}".format(filename),  # noqa
            "46 fibonacci 92                 yield x {0}".format(filename),  # noqa
            "55 fibonacci 93                 x, y = y, x + y {0}".format(filename),  # noqa
            "56 fibonacci 91             for i in range(items): {0}".format(filename),  # noqa
            "57 fibonacci 92                 yield x {0}".format(filename),  # noqa
            "66 fibonacci 93                 x, y = y, x + y {0}".format(filename),  # noqa
            "67 fibonacci 91             for i in range(items): {0}".format(filename),  # noqa
            "68 fibonacci 92                 yield x {0}".format(filename),  # noqa
            "77 fibonacci 93                 x, y = y, x + y {0}".format(filename),  # noqa
            "78 fibonacci 91             for i in range(items): {0}".format(filename),  # noqa
            "79 fibonacci 92                 yield x {0}".format(filename),  # noqa
            "88 fibonacci 93                 x, y = y, x + y {0}".format(filename),  # noqa
            "89 fibonacci 91             for i in range(items): {0}".format(filename),  # noqa
            "90 fibonacci 92                 yield x {0}".format(filename),  # noqa
            "99 fibonacci 93                 x, y = y, x + y {0}".format(filename),  # noqa
            "100 fibonacci 91             for i in range(items): {0}".format(filename),  # noqa
            "101 fibonacci 92                 yield x {0}".format(filename),  # noqa
            "110 fibonacci 93                 x, y = y, x + y {0}".format(filename),  # noqa
            "111 fibonacci 91             for i in range(items): {0}".format(filename)]  # noqa

        records = ''.join(self.stream.buflist).splitlines()
        self.assertEqual(records, expected)

    def test_function_using_tuples(self):
        filename = self.filename
        # tuple records are not compatible with the default OnValue filters.
        recorder = TextStreamRecorder(
            text_stream=self.stream,
            filter_=lambda x: x[-1] == filename)
        logger = LineMonitor(recorder, record_type=tuple)

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
            "0 gcd 153             while x > 0: {0}".format(filename),
            "1 gcd 154                 x, y = y % x, x {0}".format(filename),
            "2 gcd 153             while x > 0: {0}".format(filename),
            "3 gcd 154                 x, y = y % x, x {0}".format(filename),
            "4 gcd 153             while x > 0: {0}".format(filename),
            "5 gcd 155             return y {0}".format(filename)]
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
