# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/line_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from __future__ import absolute_import
import inspect

from pikos._internal.trace_function_manager import TraceFunctionManager
from pikos._internal.keep_track import KeepTrack
from pikos.monitors.monitor import Monitor
from pikos.monitors.records import LineRecord


class LineMonitor(Monitor):
    """ Record python line events.

    The class hooks on the settrace function to receive trace events and
    record when a line of code is about to be executed.

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
        The current zero based record index. Each `line` trace event will
        increase the index by one.

    _call_tracker : object
        An instance of the :class:`~pikos._internal.keep_track` utility class
        to keep track of recursive calls to the monitor's
        :meth:`__enter__` and :meth:`__exit__` methods.

    _record_type: class object
        A class object to be used for records. Default is
        :class:`~pikos.monitors.records.LineMonitor`

    """

    def __init__(self, recorder, record_type=None):
        """ Initialize the monitoring class.

        Parameters
        ----------
        recorder : object
            A subclass of :class:`~pikos.recorders.AbstractRecorder` or a class
            that implements the same interface to handle the values to be
            recorded.

        record_type: class object
            A class object to be used for records. Default is
            :class:`~pikos.monitors.records.LineMonitor`

        """
        self._recorder = recorder
        self._tracer = TraceFunctionManager()
        self._index = 0
        self._call_tracker = KeepTrack()
        if record_type is None:
            self._record_type = LineRecord
        else:
            self._record_type = record_type
        self._use_tuple = self._record_type is tuple

    def enable(self):
        """ Enable the monitor.

        The first time the method is called (the context is entered) it will
        set the settrace hook and initialize the recorder.

        """
        if self._call_tracker('ping'):
            self._recorder.prepare(self._record_type)
            self._tracer.replace(self.on_line_event)

    def disable(self):
        """ Disable the monitor.

        The last time the method is called (the context is exited) it will
        unset the settrace hook and finalize the recorder.

        """
        if self._call_tracker('pong'):
            self._tracer.recover()
            self._recorder.finalize()

    def on_line_event(self, frame, why, arg):
        """ Record the current line trace event.

        Called on trace events and when they refer to line traces, it will
        retrieve the necessary information from the `frame`, create a
        :class:`LineRecord` and send it to the recorder.

        """
        if why == 'line':
            record = self.gather_info(frame)
            if not self._use_tuple:
                record = self._record_type(*record)
            self._recorder.record(record)
            self._index += 1
        return self.on_line_event

    def gather_info(self, frame):
        """ Gather information into a tuple.

        """
        filename, lineno, function, line, _ = inspect.getframeinfo(
            frame, context=1)
        if line is None:
            line = ['<compiled string>']
        return self._index, function, lineno, line[0].rstrip(), filename
