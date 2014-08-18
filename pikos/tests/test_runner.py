import unittest

from pikos.runner import get_function, get_focused_on


def module_function():
    pass


class DummyClass(object):

    def method(self):
        pass


class TestRunner(unittest.TestCase):

    def test_get_module_level_function(self):
        function = get_function('pikos.tests.test_runner.module_function')
        self.assertEqual(function.func_code, module_function.func_code)

    def test_get_class_level_function(self):
        function = get_function(
            'pikos.tests.test_runner.DummyClass.method')
        self.assertEqual(function.func_code, DummyClass.method.func_code)

    def test_focused_on_script_method(self):
        functions = get_focused_on(__file__, 'module_function')
        self.assertEqual(len(functions), 1)
        function = functions[0]
        self.assertEqual(function.func_code, module_function.func_code)

    def test_get_focused_on_script_class_method(self):
        functions = get_focused_on(__file__, 'DummyClass.method')
        self.assertEqual(len(functions), 1)
        function = functions[0]
        self.assertEqual(function.func_code, DummyClass.method.func_code)

    def test_get_focused_with_multiple_functions(self):
        functions = get_focused_on(
            __file__, 'module_function, DummyClass.method')
        self.assertEqual(len(functions), 2)
        self.assertEqual(
            [functions[0].func_code, functions[1].func_code],
            [module_function.func_code, DummyClass.method.func_code])


if __name__ == '__main__':
    unittest.main()
