# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/line_memory_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from __future__ import absolute_import
import inspect
import os
from collections import namedtuple

import psutil

from pikos._internal.trace_function_manager import TraceFunctionManager
from pikos._internal.keep_track import KeepTrack
from pikos.monitors.monitor import Monitor


LINE_MEMORY_RECORD = (
        'index', 'function', 'lineNo', 'RSS', 'VMS', 'line', 'filename')
LINE_MEMORY_RECORD_TEMPLATE = (
        '{:<12} | {:<30} | {:<7} | {:>15} | {:>15} | {} {}{newline}')
LINE_MEMORY_HEADER_TEMPLATE = (
        '{:^12} | {:^30} | {:^7} | {:^15} | {:^15} | {} {}{newline}')


class LineMemoryRecord(namedtuple('LineMemoryRecord', LINE_MEMORY_RECORD)):

    __slots__ = ()

    @classmethod
    def header(cls):
        """ Return a formated header line """
        return LINE_MEMORY_HEADER_TEMPLATE.format(*cls._fields,
                                               newline=os.linesep)

    def line(self):
        """ Return a formated header line """
        return LINE_MEMORY_RECORD_TEMPLATE.format(*self, newline=os.linesep)


class LineMemoryMonitor(Monitor):
    """ Record process memory on python function events.

    The class hooks on the settrace function to receive trace events and
    record the current process memory when a line of code is about to be
    executed.

    Private
    -------
    _recorder : object
        A recorder object that implementes the
        :class:`~pikos.recorder.AbstractRecorder` interface.

    _tracer : object
        An instance of the
        :class:`~pikos._internal.trace_functions.TraceFunctionManager` utility
        class that is used to set and unset the settrace function as required
        by the monitor.

    _index : int
        The current zero based record index. Each function event will increase
        the index by one.

    _call_tracker : object
        An instance of the :class:`~pikos._internal.keep_track` utility class
        to keep track of recursive calls to the monitor's :meth:`__enter__` and
        :meth:`__exit__` methods.

    _process : object
       An instanse of :class:`psutil.Process` for the current process, used to
       get memory information in a platform independent way.

    """

    def __init__(self, recorder):
        """ Initialize the monitoring class.

        Parameters
        ----------
        recorder : object
            A subclass of :class:`~pikos.recorders.AbstractRecorder` or a
            class that implements the same interface to handle the values
            to be recorded.

        """
        self._recorder = recorder
        self._tracer = TraceFunctionManager()
        self._index = 0
        self._call_tracker = KeepTrack()
        self._process = None

    def __enter__(self):
        """ Enter the monitor context.

        The first time the method is called (the context is entered) it will
        initialize the Process class, set the settrace hook and initialize
        the recorder.

        """
        if self._call_tracker('ping'):
            self._process = psutil.Process(os.getpid())
            self._recorder.prepare(LineMemoryRecord)
            self._tracer.replace(self.on_line_event)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Exit the monitor context.

        The last time the method is called (the context is exited) it will
        unset the settrace hook, finalize the recorder and set
        :attr:`_process` to None.

        """
        if self._call_tracker('pong'):
            self._tracer.recover()
            self._recorder.finalize()

    def on_line_event(self, frame, why, arg):
        """ Record the current line trace event.

        Called on trace events and when they refer to line traces, it will
        retrieve the necessary information from the `frame` and get the
        current memory info, create a :class:`LineMemoryRecord` and send it to
        the recorder.

        """
        if why.startswith('l'):
            usage = self._process.get_memory_info()
            filename, lineno, function, line, _ = \
                inspect.getframeinfo(frame, context=1)
            if line is None:
                line = ['<compiled string>']
            record = LineMemoryRecord(self._index, function, lineno,
                                      usage.rss, usage.vms, line[0],
                                      filename)
            self._recorder.record(record)
            self._index += 1
        return self.on_line_event
