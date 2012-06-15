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
import os
import inspect

from collections import namedtuple
from pikos._internal.trace_functions import TraceFunctions
from pikos._internal.keep_track import KeepTrack


LINE_RECORD = ('index', 'function', 'lineNo', 'line', 'filename')
LINE_RECORD_TEMPLATE = '{:<12} {:<50} {:<7} {} -- {}{newline}'

class LineRecord(namedtuple('LineRecord', LINE_RECORD)):

    __slots__ = ()

    @classmethod
    def header(cls):
        """ Return a formated header line """
        return LINE_RECORD_TEMPLATE.format(*cls._fields,
                                               newline=os.linesep)

    def line(self):
        """ Return a formated header line """
        return LINE_RECORD_TEMPLATE.format(*self, newline=os.linesep)

class LineMonitor(object):
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
        :class:`~pikos._internal.trace_functions.TraceFunctions` utility
        class that is used to set and unset the settrace function as required
        by the monitor.

    _index : int
        The current zero based record index. Each `line` trace event will
        increase the index by one.

    _call_tracker : object
        An instance of the :class:`~pikos._internal.keep_track` utility class
        to keep track of recursive calls to the monitor's :meth:`__enter__` and
        :meth:`__exit__` methods.

    """

    def __init__(self, recorder):
        """ Initialize the monitoring class.

        Parameters
        ----------
        recorder : object
            A subclass of :class:`~pikos.recorders.AbstractRecorder` or a class
            that implements the same interface to handle the values to be
            recorded.

        """
        self._recorder = recorder
        self._tracer = TraceFunctions()
        self._index = 0
        self._call_tracker = KeepTrack()

    def __enter__(self):
        """ Enter the monitor context.

        The first time the method is called (the context is entered) it will
        set the settrace hook and initialize the recorder.

        """
        if self._call_tracker('ping'):
            self._recorder.prepare(LineRecord)
            self._tracer.set(self.on_line_event)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Exit the monitor context.

        The last time the method is called (the context is exited) it will
        unset the settrace hook and finalize the recorder.

        """
        if self._call_tracker('pong'):
            self._tracer.unset()
            self._recorder.finalize()

    def on_line_event(self, frame, why, arg):
        """ Record the current line trace event.

        Called on trace events and when they refer to line traces, it will
        retrieve the necessary information from the `frame`, create a
        :class:`LineRecord` and send it to the recorder.

        """
        if why == 'line':
            filename, lineno, function, line, _ = \
                inspect.getframeinfo(frame, context=1)
            if line is None:
                line = ['<compiled string>']
            record = LineRecord(self._index, function, lineno,
                                line[0].rstrip(), filename)
            self._recorder.record(record)
            self._index += 1
        return self.on_line_event
