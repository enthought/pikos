# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: api.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import warnings

from pikos.monitors.monitor_attach import MonitorAttach


def screen(filter_=None):
    """ Factory function that returns a basic recorder that outputs to screen

    Parameters
    ----------
    filter_ : callable
        A callable function that accepts a data tuple and returns True
        if the input sould be recorded. Default is None.

    """
    import sys
    from pikos.recorders.text_stream_recorder import TextStreamRecorder
    return TextStreamRecorder(
        sys.stdout, filter_=filter_, auto_flush=True, formatted=True)


def textfile(filename=None, filter_=None):
    """ Factory function that returns a basic recorder that outputs to file.

    Parameters
    ----------
    filename: string
        The name and path of the file where to store the records. Default
        name is "monitor_records.txt".

    filter_ : callable
        A callable function that accepts a data tuple and returns True
        if the input sould be recorded. Default is None.

    """
    if filename is None:
        filename = 'monitor_records.log'
    from pikos.recorders.text_file_recorder import TextFileRecorder
    return TextFileRecorder(
        filename, filter_=filter_, auto_flush=True, formatted=True)


def csvfile(filename=None, filter_=None):
    """ Factory function that returns a basic recorder that outputs to file.

    Parameters
    ----------
    filename : string
        The name and path of the file where to store the records. Default
        name is "monitor_records.txt".

    filter_ : callable
        A callable function that accepts a data tuple and returns True
        if the input sould be recorded. Default is None.

    """
    if filename is None:
        filename = 'monitor_records.csv'
    from pikos.recorders.csv_file_recorder import CSVFileRecorder
    return CSVFileRecorder(
        filename, filter_=filter_)


def monitor_functions(recorder=None, focus_on=None):
    """ Factory function that returns a basic function monitor.

    Parameters
    ----------
    recorder : AbstractRecorder
        The recorder to use and store the records. Default is outout to screen.

    focus_on : list
        The list of function where to focus monitoring.

    """
    if recorder is None:
        recorder = screen()
    if focus_on is None:
        try:
            from pikos.cymonitors.api import FunctionMonitor
        except ImportError:
            from pikos.monitors.api import FunctionMonitor
            warnings.warn(
                'Cython monitors are not available '
                'falling back to pure python')
        monitor = FunctionMonitor(recorder)
    else:
        from pikos.monitors.focused_function_monitor import (
            FocusedFunctionMonitor)
        monitor = FocusedFunctionMonitor(recorder, functions=focus_on)
    return MonitorAttach(monitor)


def monitor_lines(recorder=None, focus_on=None):
    """ Factory function that returns a basic line monitor.

    Parameters
    ----------
    recorder : AbstractRecorder
        The recorder to use and store the records. Default is outout to screen.

    focus_on : list
        The list of function where to focus monitoring.

    """
    if recorder is None:
        recorder = screen()
    if focus_on is None:
        from pikos.monitors.line_monitor import LineMonitor
        monitor = LineMonitor(recorder)
    else:
        from pikos.monitors.focused_line_monitor import FocusedLineMonitor
        monitor = FocusedLineMonitor(recorder, functions=focus_on)
    return MonitorAttach(monitor)


def memory_on_functions(recorder=None, focus_on=None):
    """ Factory function that returns a basic function memory monitor.

    Parameters
    ----------
    recorder : AbstractRecorder
        The recorder to use and store the records. Default is outout to screen.

    focus_on : list
        The list of function where to focus monitoring.

    """
    if recorder is None:
        recorder = screen()
    if focus_on is None:
        from pikos.monitors.function_memory_monitor import (
            FunctionMemoryMonitor)
        monitor = FunctionMemoryMonitor(recorder)
    else:
        from pikos.monitors.focused_function_memory_monitor import (
            FocusedFunctionMemoryMonitor)
        monitor = FocusedFunctionMemoryMonitor(recorder, functions=focus_on)

    return MonitorAttach(monitor)


def memory_on_lines(recorder=None, focus_on=None):
    """ Factory function that returns a basic line memory monitor.

    Parameters
    ----------
    recorder : AbstractRecorder
        The recorder class to use and store the records. Default is outout to
        screen.

    focus_on : list
        The list of function where to focus monitoring.

    """
    if recorder is None:
        recorder = screen()
    if focus_on is None:
        from pikos.monitors.line_memory_monitor import LineMemoryMonitor
        monitor = LineMemoryMonitor(recorder)
    else:
        from pikos.monitors.focused_line_memory_monitor import (
            FocusedLineMemoryMonitor)
        monitor = FocusedLineMemoryMonitor(recorder, functions=focus_on)
    return MonitorAttach(monitor)
