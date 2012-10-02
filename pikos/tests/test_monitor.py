import unittest

from pikos.monitor import Monitor as monitor


# FIXME: might be better to use a mock library
class MockNativeMonitor():

    def __init__(self):
        self._enter_called = 0
        self._exit_called = 0

    def __enter__(self):
        self._enter_called += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._exit_called += 1


class TestMonitor(unittest.TestCase):

    def test_function_with_context_manager(self):

        mock_logger = MockNativeMonitor()

        @monitor(mock_logger)
        def my_function(value):
            return "I was called with {}".format(value)

        result = my_function(5)
        self.assertEqual(mock_logger._enter_called, 1)
        self.assertEqual(mock_logger._exit_called, 1)
        self.assertEqual(result, "I was called with 5")

    def test_recursive_with_context_manager(self):
        mock_logger = MockNativeMonitor()

        @monitor(mock_logger)
        def gcd(x, y):
            return x if y == 0 else gcd(y, (x % y))

        result = gcd(21, 28)
        self.assertEqual(mock_logger._enter_called, 4)
        self.assertEqual(mock_logger._exit_called, 4)
        self.assertEqual(result, 7)

    def test_generator_with_context_manager(self):

        mock_logger = MockNativeMonitor()

        @monitor(mock_logger)
        def my_generator(value):
            for i in range(value):
                yield i

        results = []
        for i in my_generator(5):
            results.append(i)

        self.assertEqual(results, [0, 1, 2, 3, 4])
        self.assertEqual(mock_logger._enter_called, 6)
        self.assertEqual(mock_logger._exit_called, 6)


if __name__ == '__main__':
    unittest.main()
