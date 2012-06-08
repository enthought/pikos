# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: api.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------

from pikos.monitor import Monitor

def baserecorder(filter_=None):
    """ Factory function that returns a basic recorder.
    """
    import sys
    from pikos.recorders.text_stream_recorder import TextStreamRecorder
    return TextStreamRecorder(sys.stdout, filter_=filter_, auto_flush=True)

def monitor_functions(filter_=None):
    """ Factory function that returns a basic function monitor.
    """
    from pikos.monitors.function_monitor import FunctionMonitor
    return Monitor(FunctionMonitor(baserecorder(filter_=filter_)))

def monitor_lines(filter_=None):
    """ Factory function that returns a basic line monitor.
    """
    from pikos.monitors.line_monitor import LineMonitor
    return Monitor(LineMonitor(baserecorder(filter_=filter_)))

def memory_on_functions(filter_=None):
    """ Factory function that returns a basic function memory monitor.
    """
    from pikos.monitors.function_memory_monitor import FunctionMemoryMonitor
    return Monitor(FunctionMemoryMonitor(baserecorder(filter_=filter_)))

def memory_on_lines(filter_=None):
    """ Factory function that returns a basic line memory monitor.
    """
    from pikos.monitors.line_memory_monitor import LineMemoryMonitor
    return Monitor(LineMemoryMonitor(baserecorder(filter_=filter_)))

def yappi_profile(buildins=None):
    """ Factory function that returns a yappi monitor.
    """
    from pikos.external.yappi_profiler import YappiProfiler
    return Monitor(YappiProfiler(buildins))

def line_profile(*args, **kwrds):
    """ Factory function that returns a line profiler.

    Please refer to
    `<http://packages.python.org/line_profiler/ for more information>_`
    for initialization options.
    """
    from pikos.external.line_profiler import LineProfiler
    return Monitor(LineProfiler(*args, **kwrds))


#: Easy to find placeholder for the Monitor decorator class.
monitor = Monitor
