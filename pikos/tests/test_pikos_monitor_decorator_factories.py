# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: tests/test_pikos_monitor_decorator_factories.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
# -----------------------------------------------------------------------------
from pikos.monitors.api import MonitorAttach
from pikos.recorders.api import ListRecorder, TextStreamRecorder
from pikos.tests import compat


class TestPikosRecorderFactories(compat.TestCase):

    def test_monitor_functions(self):
        from pikos.api import monitor_functions

        # The default behaviour will use the cython monitors if available.
        try:
            from pikos.cymonitors.api import FunctionMonitor
        except ImportError:
            from pikos.monitors.api import FunctionMonitor
        from pikos.monitors.api import FocusedFunctionMonitor

        self.check_monitor_decorator(monitor_functions, FunctionMonitor)
        self.check_focused_monitor_decorator(
            monitor_functions, FocusedFunctionMonitor)

    def test_monitor_lines(self):
        from pikos.api import monitor_lines
        from pikos.monitors.api import LineMonitor, FocusedLineMonitor

        self.check_monitor_decorator(monitor_lines, LineMonitor)
        self.check_focused_monitor_decorator(
            monitor_lines, FocusedLineMonitor)

    def test_memory_on_functions(self):
        self.check_for_psutils()
        from pikos.api import memory_on_functions
        from pikos.monitors.api import (
            FunctionMemoryMonitor, FocusedFunctionMemoryMonitor)

        self.check_monitor_decorator(
            memory_on_functions, FunctionMemoryMonitor)
        self.check_focused_monitor_decorator(
            memory_on_functions, FocusedFunctionMemoryMonitor)

    def test_memory_on_lines(self):
        self.check_for_psutils()
        from pikos.api import memory_on_lines
        from pikos.monitors.api import (
            LineMemoryMonitor, FocusedLineMemoryMonitor)

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

    def check_for_psutils(self):
        try:
            import psutil  # noqa
        except ImportError:
            self.skipTest('Could not import psutils, skipping test.')


if __name__ == '__main__':
    import unittest
    unittest.main()
