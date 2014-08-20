import contextlib
import os
import sys
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
        filename = self._script_file()
        with self._python_path(filename):
            functions = get_focused_on(filename, 'module_function')
        self.assertEqual(len(functions), 1)
        function = functions[0]
        self.assertEqual(function.func_code, module_function.func_code)

    def test_get_focused_on_script_class_method(self):
        filename = self._script_file()
        with self._python_path(filename):
            functions = get_focused_on(filename, 'DummyClass.method')
        self.assertEqual(len(functions), 1)
        function = functions[0]
        self.assertEqual(function.func_code, DummyClass.method.func_code)

    def test_get_focused_with_multiple_functions(self):
        filename = self._script_file()
        with self._python_path(filename):
            functions = get_focused_on(
                filename, 'module_function, DummyClass.method')
        self.assertEqual(len(functions), 2)
        self.assertEqual(
            [functions[0].func_code, functions[1].func_code],
            [module_function.func_code, DummyClass.method.func_code])

    def _script_file(self):
        module_file = os.path.splitext(__file__)[0]
        return '.'.join((module_file, 'py'))

    @contextlib.contextmanager
    def _python_path(self, path):
        self = os.path.dirname(path)
        sys.path.insert(0, self)
        try:
            yield
        finally:
            sys.path.remove(self)


if __name__ == '__main__':
    unittest.main()
