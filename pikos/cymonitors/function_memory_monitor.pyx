# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: cymonitors/c_function_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#----------------------------------------------------------------------------
from cpython.pystate cimport (
    PyTrace_CALL, PyTrace_EXCEPTION, PyTrace_RETURN,  Py_tracefunc,
    PyTrace_C_CALL, PyTrace_C_EXCEPTION, PyTrace_LINE, PyTrace_C_RETURN)

from .monitor cimport Monitor
from .pytrace cimport PyEval_SetProfile, PyFrameObject

import os
import psutil

from pikos._internal.keep_track import KeepTrack
from pikos.monitors.records import FunctionMemoryRecord


cdef class FunctionMemoryMonitor(Monitor):
    """ Record process memory on python function events.

    The class hooks on the setprofile function to receive function events and
    record the current process memory when they happen.

    Private
    -------
    _recorder : object
        A recorder object that implementes the
        :class:`~pikos.recorder.AbstractRecorder` interface.

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

    _record_type : object
        A class object to be used for records. Default is
        :class:`~pikos.monitors.records.FunctionMemoryMonitor`

    _record_type: class object
        A class object to be used for records. Default is
        :class:`~pikos.monitors.records.FunctionMemoryMonitor`

    """

    cdef public object _recorder
    cdef public object record_type
    cdef int _index
    cdef object _call_tracker
    cdef object _process

    def __init__(self, recorder, record_type=None):
        """ Constructor

        Parameters
        ----------
        recorder : Recorder
            The recorder inctance to use.

        record_type :
            The record type to use. Default is to use a FunctionRecord.

        """
        self._recorder = recorder
        self._call_tracker = KeepTrack()
        self._process = None
        if record_type is None:
            self.record_type = FunctionMemoryRecord
        else:
            self.record_type = record_type

    def enable(self):
        """ Enable the monitor.

        The first time the method is called (the context is entered) it will
        set the setprofile hooks and initialize the recorder.

        """
        if self._call_tracker('ping'):
            self._process = psutil.Process(os.getpid())
            self._recorder.prepare(self.record_type)
            if self.record_type == tuple:
                # optimized function for tuples.
                PyEval_SetProfile(
                    <Py_tracefunc>self.on_function_event_tuple, self)
            else:
                PyEval_SetProfile(<Py_tracefunc>self.on_function_event, self)

    def disable(self):
        """ Disable the monitor.

        The last time the method is called (the context is exited) it will
        unset the setprofile hooks and finalize the recorder.

        """
        if self._call_tracker('pong'):
            PyEval_SetProfile(NULL, None)
            self._recorder.finalize()
            self._process = None

    cdef int on_function_event(
            self, PyFrameObject *_frame, int event, object arg) except -1:
        """ Record the current function event.

        Called on function events, it will retrieve the necessary information
        from the `frame`, create a :class:`FunctionRecord` and send it to the
        recorder.

        """
        cdef:
            object frame = <object>_frame
            object record

        if event < PyTrace_C_CALL:
            function = frame.f_code.co_name
        else:
            function = arg.__name__

        if event == PyTrace_CALL:
            event_str = 'call'
        elif event == PyTrace_RETURN:
            event_str = 'return'
        elif event == PyTrace_C_CALL:
            event_str = 'c_call'
        elif event == PyTrace_C_RETURN:
            event_str = 'c_return'
        elif event == PyTrace_EXCEPTION:
            event_str = 'exception'
        elif event == PyTrace_C_EXCEPTION:
            event_str = 'c_exception'
        else:
            raise RuntimeError('Unknown profile event %s' % event)

        rss, vms = self._process.memory_info()
        record = self.record_type(
            self._index, event_str, function, rss, vms, frame.f_lineno,
            frame.f_code.co_filename)

        self._recorder.record(record)

        self._index += 1
        return 0

    cdef int on_function_event_tuple(
            self, PyFrameObject *_frame, int event, object arg) except -1:
        """ Record the current function event.

        Called on function events, it will retrieve the necessary information
        from the `frame`, create a :class:`FunctionRecord` and send it to the
        recorder.

        """
        cdef:
            object frame = <object>_frame
            object record

        if event < PyTrace_C_CALL:
            function = frame.f_code.co_name
        else:
            function = arg.__name__

        if event == PyTrace_CALL:
            event_str = 'call'
        elif event == PyTrace_RETURN:
            event_str = 'return'
        elif event == PyTrace_C_CALL:
            event_str = 'c_call'
        elif event == PyTrace_C_RETURN:
            event_str = 'c_return'
        elif event == PyTrace_EXCEPTION:
            event_str = 'exception'
        elif event == PyTrace_C_EXCEPTION:
            event_str = 'c_exception'
        else:
            raise RuntimeError('Unknown profile event %s' % event)

        rss, vms = self._process.memory_info()
        record = (
            self._index, event_str, function, rss, vms, frame.f_lineno,
            frame.f_code.co_filename)

        self._recorder.record(record)

        self._index += 1
        return 0
