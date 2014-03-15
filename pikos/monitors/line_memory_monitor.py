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

import psutil

from pikos._internal.trace_function_manager import TraceFunctionManager
from pikos._internal.keep_track import KeepTrack
from pikos.monitors.monitor import Monitor
from pikos.monitors.records import LineMemoryRecord


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

    _record_type: class object
        A class object to be used for records. Default is
        :class:`~pikos.monitors.records.LineMemoryMonitor`

    """

    def __init__(self, recorder, record_type=None):
        """ Initialize the monitoring class.

        Parameters
        ----------
        recorder : object
            A subclass of :class:`~pikos.recorders.AbstractRecorder` or a
            class that implements the same interface to handle the values
            to be recorded.

        record_type: class object
            A class object to be used for records. Default is
            :class:`~pikos.monitors.records.LineMemoryMonitor`

        """
        self._recorder = recorder
        self._tracer = TraceFunctionManager()
        self._index = 0
        self._call_tracker = KeepTrack()
        self._process = None
        if record_type is None:
            self._record_type = LineMemoryRecord
        else:
            self._record_type = record_type

    def enable(self):
        """ Enable the monitor.

        The first time the method is called (the context is entered) it will
        initialize the Process class, set the settrace hook and initialize
        the recorder.

        """
        if self._call_tracker('ping'):
            self._process = psutil.Process(os.getpid())
            self._recorder.prepare(self._record_type)
            if self._record_type is tuple:
                # optimized function for tuples.
                self._tracer.replace(self.on_line_event_using_tuple)
            else:
                self._tracer.replace(self.on_line_event)

    def disable(self):
        """ Disable the monitor.

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
            record = self._record_type(
                self._index, function, lineno, usage[0], usage[1], line[0],
                filename)
            self._recorder.record(record)
            self._index += 1
        return self.on_line_event

    def on_line_event_using_tuple(self, frame, why, arg):
        """ Record the current line trace events optimized using tuples.

        """
        if why.startswith('l'):
            usage = self._process.get_memory_info()
            filename, lineno, function, line, _ = \
                inspect.getframeinfo(frame, context=1)
            if line is None:
                line = ['<compiled string>']
            record = (
                self._index, function, lineno, usage[0], usage[1], line[0],
                filename)
            self._recorder.record(record)
            self._index += 1
        return self.on_line_event_using_tuple
