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
import inspect
from collections import namedtuple

from pikos._internal.profile_function_manager import ProfileFunctionManager
from pikos._internal.keep_track import KeepTrack
from pikos.monitors.monitor import Monitor
from pikos.monitors.records import FunctionRecord


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

    _record: function object
        The cached reference to the record function.

    _record_type: class object
        A class object to be used for records. Default is
        :class:`~pikos.monitors.records.FunctionMonitor`

    """

    def __init__(self, recorder, record_type=None):
        """ Initialize the monitoring class.

        Parameters
        ----------
        recorder : object
            A subclass of :class:`~pikos.recorders.AbstractRecorder` or a class
            that implements the same interface to handle the values to be
            logged.

        record_type: class object
            A class object to be used for records. Default is
            :class:`~pikos.monitors.records.FunctionMonitor.

        """
        self._recorder = recorder
        self._record = recorder.record
        self._profiler = ProfileFunctionManager()
        self._index = 0
        self._call_tracker = KeepTrack()
        if record_type is None:
            self._record_type = FunctionRecord
        else:
            self._record_type = record_type
            if record_type is tuple:
                # optimized function for tuples.
                self.on_function_event = self._on_function_event_tuple

    def enable(self):
        """ Enable the monitor.

        The first time the method is called (the context is entered) it will
        set the setprofile hooks and initialize the recorder.

        """
        if self._call_tracker('ping'):
            self._recorder.prepare(self._record_type)
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
        if '_' == event[1]:
            record = self._record_type(
                self._index, event, arg.__name__,
                frame.f_lineno, frame.f_code.co_filename)
        else:
            code = frame.f_code
            record = self._record_type(
                self._index, event, code.co_name,
                frame.f_lineno, code.co_filename)
        self._record(record)
        self._index += 1

    def _on_function_event_tuple(self, frame, event, arg):
        """ Record the current function event using a tuple.

        Called on function events, it will retrieve the necessary information
        from the `frame`, create a :class:`FunctionRecord` and send it to the
        recorder.

        """
        if '_' == event[1]:
            record = (
                self._index, event, arg.__name__,
                frame.f_lineno, frame.f_code.co_filename)
        else:
            code = frame.f_code
            record = (
                self._index, event, code.co_name,
                frame.f_lineno, code.co_filename)
        self._record(record)
        self._index += 1
