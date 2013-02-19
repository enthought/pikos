# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: api.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from pikos.monitors.monitor_attach import MonitorAttach


def baserecorder(filter_=None):
    """ Factory function that returns a basic recorder.
    """
    import sys
    from pikos.recorders.text_stream_recorder import TextStreamRecorder
    return TextStreamRecorder(sys.stdout, filter_=filter_,
                               auto_flush=True, formatted=True)


def monitor_functions(filter_=None, focus_on=None):
    """ Factory function that returns a basic function monitor.
    """
    if focus_on is None:
        from pikos.monitors.function_monitor import FunctionMonitor
        monitor = FunctionMonitor(baserecorder(filter_=filter_))
    else:
        from pikos.monitors.focused_function_monitor import \
            FocusedFunctionMonitor
        monitor = FocusedFunctionMonitor(baserecorder(filter_=filter_),
                                  functions=focus_on)
    return MonitorAttach(monitor)


def monitor_lines(filter_=None, focus_on=None):
    """ Factory function that returns a basic line monitor.
    """
    if focus_on is None:
        from pikos.monitors.line_monitor import LineMonitor
        monitor = LineMonitor(baserecorder(filter_=filter_))
    else:
        from pikos.monitors.focused_line_monitor import FocusedLineMonitor
        monitor = FocusedLineMonitor(baserecorder(filter_=filter_),
                                     functions=focus_on)
        return MonitorAttach(monitor)


def memory_on_functions(filter_=None, focus_on=None):
    """ Factory function that returns a basic function memory monitor.
    """
    if focus_on is None:
        from pikos.monitors.function_memory_monitor import \
            FunctionMemoryMonitor
        monitor = FunctionMemoryMonitor(baserecorder(filter_=filter_))
    else:
        from pikos.monitors.focused_function_memory_monitor import\
            FocusedFunctionMemoryMonitor
        monitor = FocusedFunctionMemoryMonitor(baserecorder(filter_=filter_),
                                               functions=focus_on)
    return MonitorAttach(monitor)


def memory_on_lines(filter_=None, focus_on=None):
    """ Factory function that returns a basic line memory monitor.
    """
    if focus_on is None:
        from pikos.monitors.line_memory_monitor import LineMemoryMonitor
        monitor = LineMemoryMonitor(baserecorder(filter_=filter_))
    else:
        from pikos.monitors.focused_line_memory_monitor import \
            FocusedLineMemoryMonitor
        monitor = FocusedLineMemoryMonitor(baserecorder(filter_=filter_),
                                           functions=focus_on)
    return MonitorAttach(monitor)


def yappi_profile(buildins=None):
    """ Factory function that returns a yappi monitor.
    """
    from pikos.external.yappi_profiler import YappiProfiler
    return MonitorAttach(YappiProfiler(buildins))


def line_profile(*args, **kwrds):
    """ Factory function that returns a line profiler.

    Please refer to
    `<http://packages.python.org/line_profiler/ for more information>_`
    for initialization options.
    """
    from pikos.external.line_profiler import LineProfiler
    return MonitorAttach(LineProfiler(*args, **kwrds))


#: Easy to find placeholder for the Monitor decorator class.
monitor_attach = MonitorAttach
