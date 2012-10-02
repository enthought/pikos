import unittest

from pikos.monitor import Monitor as monitor
from pikos.monitors.function_memory_monitor import FunctionMemoryMonitor
from pikos.recorders.list_recorder import ListRecorder
from pikos.tests.test_assistant import TestAssistant


class TestFunctionMemoryMonitor(unittest.TestCase, TestAssistant):

    def test_function(self):
        recorder = ListRecorder()
        logger = FunctionMemoryMonitor(recorder)

        @monitor(logger)
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
        records = recorder.records
        # check that the records make sense
        self.assertFieldValueExist(records, ('function', 'type'),
                                   ('gcd', 'call'), times=1)
        self.assertFieldValueExist(records, ('function', 'type'),
                                   ('gcd', 'return'), times=1)
        self.assertFieldValueNotExist(records, ('function',), ('boo',))
        # The wrapper of the function should not be logged
        self.assertFieldValueNotExist(records, ('function',), ('wrapper',))

    def test_recursive(self):
        recorder = ListRecorder()
        logger = FunctionMemoryMonitor(recorder)

        @monitor(logger)
        def gcd(x, y):
            return x if y == 0 else gcd(y, (x % y))

        def boo():
            return gcd(7, 12)

        result = boo()
        self.assertEqual(result, 1)
        records = recorder.records
        # check that the records make sense
        # The function should be called 6 times
        self.assertFieldValueExist(records, ('function', 'type'),
                                   ('gcd', 'call'), times=6)
        self.assertFieldValueExist(records, ('function', 'type'),
                                   ('gcd', 'return'), times=6)
        self.assertFieldValueNotExist(records, ('function',), ('boo',))
        # In recursive calls the wrapper of the function is logged
        # self.assertFieldValueNotExist(records, ('function',), ('wrapper',))

    def test_generator(self):
        recorder = ListRecorder()
        logger = FunctionMemoryMonitor(recorder)
        output = (0, 1, 1, 2, 3, 5, 8, 13, 21, 34)

        @monitor(logger)
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
        records = recorder.records
        # check that the records make sense
        # The function should be called 10 + 1 times
        self.assertFieldValueExist(records, ('function', 'type'),
                                   ('fibonacci', 'call'), times=11)
        self.assertFieldValueExist(records, ('function', 'type'),
                                   ('fibonacci', 'return'), times=11)
        self.assertFieldValueNotExist(records, ('function',), ('boo',))
        # The wrapper of the generator should not be logged
        self.assertFieldValueNotExist(records, ('function',), ('wrapper',))

if __name__ == '__main__':
    unittest.main()
