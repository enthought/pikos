# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/function_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from __future__ import absolute_import
import os
import inspect
from collections import namedtuple

from pikos._internal.profile_function_manager import ProfileFunctionManager
from pikos._internal.keep_track import KeepTrack
from pikos.monitors.monitor import Monitor

FUNCTION_RECORD = ('index', 'type', 'function', 'lineNo', 'filename')
FUNCTION_RECORD_TEMPLATE = '{:<8} {:<11} {:<30} {:<5} {}{newline}'


class FunctionRecord(namedtuple('FunctionRecord', FUNCTION_RECORD)):

    __slots__ = ()

    @classmethod
    def header(cls):
        """ Return a formatted header line """
        return FUNCTION_RECORD_TEMPLATE.format(*cls._fields,
                                               newline=os.linesep)

    def line(self):
        """ Return a formatted header line """
        return FUNCTION_RECORD_TEMPLATE.format(*self, newline=os.linesep)


class FunctionMonitor(Monitor):
    """ Record python function events.

    The class hooks on the setprofile function to receive function events and
    record them.

    Private
    -------
    _recorder : object
        A recorder object that implementes the
        :class:`~pikos.recorder.AbstractRecorder` interface.

    _profiler : object
        An instance of the
        :class:`~pikos._internal.profiler_functions.ProfilerFunctions` utility
        class that is used to set and unset the setprofile function as required
        by the monitor.

    _index : int
        The current zero based record index. Each function event will increase
        the index by one.

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
            logged.

        """
        self._recorder = recorder
        self._profiler = ProfileFunctionManager()
        self._index = 0
        self._call_tracker = KeepTrack()

    def enable(self):
        """ Enable the monitor.

        The first time the method is called (the context is entered) it will
        set the setprofile hooks and initialize the recorder.

        """
        if self._call_tracker('ping'):
            self._recorder.prepare(FunctionRecord)
            self._profiler.replace(self.on_function_event)

    def disable(self):
        """ Disable the monitor.

        The last time the method is called (the context is exited) it will
        unset the setprofile hooks and finalize the recorder.

        """
        if self._call_tracker('pong'):
            self._profiler.recover()
            self._recorder.finalize()

    def on_function_event(self, frame, event, arg):
        """ Record the current function event.

        Called on function events, it will retrieve the necessary information
        from the `frame`, create a :class:`FunctionRecord` and send it to the
        recorder.

        """
        filename, lineno, function, _, _ = \
            inspect.getframeinfo(frame, context=0)
        if event.startswith('c_'):
            function = arg.__name__
        record = FunctionRecord(self._index, event,
                                function, lineno, filename)
        self._recorder.record(record)
        self._index += 1
