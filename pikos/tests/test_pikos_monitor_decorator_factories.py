from pikos.monitors.api import (
    FunctionMonitor, MonitorAttach, LineMonitor, FunctionMemoryMonitor,
    LineMemoryMonitor, FocusedFunctionMonitor, FocusedLineMemoryMonitor,
    FocusedLineMonitor, FocusedFunctionMemoryMonitor)
from pikos.recorders.api import ListRecorder, TextStreamRecorder
from pikos.tests import compat


class TestPikosRecorderFactories(compat.TestCase):

    def test_monitor_functions(self):
        from pikos.api import monitor_functions
        self.check_monitor_decorator(monitor_functions, FunctionMonitor)
        self.check_focused_monitor_decorator(
            monitor_functions, FocusedFunctionMonitor)

    def test_monitor_lines(self):
        from pikos.api import monitor_lines
        self.check_monitor_decorator(monitor_lines, LineMonitor)
        self.check_focused_monitor_decorator(
            monitor_lines, FocusedLineMonitor)

    def test_memory_on_functions(self):
        from pikos.api import memory_on_functions
        self.check_monitor_decorator(
            memory_on_functions, FunctionMemoryMonitor)
        self.check_focused_monitor_decorator(
            memory_on_functions, FocusedFunctionMemoryMonitor)

    def test_memory_on_lines(self):
        from pikos.api import memory_on_lines
        self.check_monitor_decorator(memory_on_lines, LineMemoryMonitor)
        self.check_focused_monitor_decorator(
            memory_on_lines, FocusedLineMemoryMonitor)

    def check_monitor_decorator(self, monitor_factory, monitor_type):
        # default usage
        decorator = monitor_factory()
        self.assertIsInstance(decorator, MonitorAttach)
        self.assertIsInstance(decorator._monitor_object, monitor_type)
        self.assertIsInstance(
            decorator._monitor_object._recorder, TextStreamRecorder)

        # with a recorder
        decorator = monitor_factory(recorder=ListRecorder())
        self.assertIsInstance(decorator, MonitorAttach)
        self.assertIsInstance(decorator._monitor_object, monitor_type)
        self.assertIsInstance(
            decorator._monitor_object._recorder, ListRecorder)

    def check_focused_monitor_decorator(self, monitor_factory, monitor_type):
        # default usage
        decorator = monitor_factory(focus_on=[self.check_monitor_decorator])
        self.assertIsInstance(decorator, MonitorAttach)
        self.assertIsInstance(decorator._monitor_object, monitor_type)
        self.assertIsInstance(
            decorator._monitor_object._recorder, TextStreamRecorder)

        # with a recorder
        decorator = monitor_factory(
            recorder=ListRecorder(), focus_on=[self.check_monitor_decorator])
        self.assertIsInstance(decorator, MonitorAttach)
        self.assertIsInstance(decorator._monitor_object, monitor_type)
        self.assertIsInstance(
            decorator._monitor_object._recorder, ListRecorder)


if __name__ == '__main__':
    import unittest
    unittest.main()
