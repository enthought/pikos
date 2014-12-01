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

from pikos._internal.profile_function_manager import ProfileFunctionManager
from pikos._internal.keep_track import KeepTrack
from pikos.monitors.monitor import Monitor
from pikos.monitors.records import FunctionRecord


class FunctionMonitor(Monitor):
    """ Record python function events.

    The class hooks on the setprofile function to receive function events and
    record them.

    """

    def __init__(self, recorder, record_type=None):
        """ Initialize the monitoring class.

        Parameters
        ----------
        recorder : object
            A subclass of :class:`~.AbstractRecorder` or a class that
            implements the same interface to handle the values to be logged.

        record_type : type
            A class object to be used for records. Default is
            :class:`~.FunctionRecord`.

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
        self._use_tuple = self._record_type is tuple

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
        record = self.gather_info(frame, event, arg)
        if not self._use_tuple:
            record = self._record_type(*record)
        self._record(record)
        self._index += 1

    def gather_info(self, frame, event, arg):
        """ Gather information for the record.

        """
        if '_' == event[1]:
            return (
                self._index, event, arg.__name__,
                frame.f_lineno, frame.f_code.co_filename)
        else:
            code = frame.f_code
            return (
                self._index, event, code.co_name,
                frame.f_lineno, code.co_filename)
