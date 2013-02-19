import unittest

from pikos._internal.function_set import FunctionSet
from pikos.tests.compat import TestCase


class TestFunctionSet(TestCase):

    def setUp(self):

        def function1():
            return 'function1'

        def function2():
            return 'function2'

        def function3():
            return 'function3'

        self.functions = [function1, function2, function3]

    def test_len(self):
        function_set = FunctionSet(self.functions)
        self.assertEqual(len(function_set), 3)

    def test_contains(self):
        function_set = FunctionSet(self.functions)
        # check contains with a function object
        self.assertIn(self.functions[0], function_set)
        self.assertIn(self.functions[1], function_set)
        self.assertIn(self.functions[2], function_set)

        # check contains with a code object
        self.assertIn(self.functions[0].func_code, function_set)
        self.assertIn(self.functions[1].func_code, function_set)
        self.assertIn(self.functions[2].func_code, function_set)

    def test_iteration(self):
        function_set = FunctionSet(self.functions)
        for function in function_set:
            self.assertIn(function, self.functions)

    def test_add(self):
        function_set = FunctionSet(self.functions)

        def function4():
            return 'function4'

        function_set.add(function4)
        self.assertIn(function4, function_set)
        self.assertEqual(len(function_set), 4)

        function_set.add(self.functions[1])
        self.assertIn(self.functions[1], function_set)
        self.assertEqual(len(function_set), 4)

    def test_discard(self):
        function_set = FunctionSet(self.functions)

        function_set.discard(self.functions[1])
        self.assertNotIn(self.functions[1], function_set)
        self.assertEqual(len(function_set), 2)


if __name__ == '__main__':
    unittest.main()
