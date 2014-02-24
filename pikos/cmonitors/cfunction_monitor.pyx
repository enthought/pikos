# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: cmonitors/c_function_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#----------------------------------------------------------------------------
from cpython.pystate cimport (
    PyTrace_CALL, PyTrace_EXCEPTION, PyTrace_RETURN,  Py_tracefunc,
    PyTrace_C_CALL, PyTrace_C_EXCEPTION, PyTrace_LINE, PyTrace_C_RETURN)

from .cmonitor cimport CMonitor
from .pytrace cimport PyEval_SetProfile, PyFrameObject

from pikos._internal.keep_track import KeepTrack
from pikos.monitors.function_monitor import FunctionRecord

trace_str = {
    PyTrace_CALL:        'call',
    PyTrace_EXCEPTION:   'exception',
    PyTrace_LINE:        'line',
    PyTrace_RETURN:      'return',
    PyTrace_C_CALL:      'c_call',
    PyTrace_C_EXCEPTION: 'c_exception',
    PyTrace_C_RETURN:    'c_return',
}.get

cdef class CFunctionMonitor(CMonitor):

    cdef public object _recorder
    cdef int _index
    cdef object _call_tracker

    def __cinit__(self, recorder):
        self._index = 0

    def __init__(self, recorder):
        self._recorder = recorder
        self._call_tracker = KeepTrack()

    def enable(self):
        """ Enable the monitor.

        The first time the method is called (the context is entered) it will
        set the setprofile hooks and initialize the recorder.

        """
        if self._call_tracker('ping'):
            self._recorder.prepare(FunctionRecord)
            PyEval_SetProfile(<Py_tracefunc>self.on_function_event, self)

    def disable(self):
        """ Disable the monitor.

        The last time the method is called (the context is exited) it will
        unset the setprofile hooks and finalize the recorder.

        """
        if self._call_tracker('pong'):
            PyEval_SetProfile(NULL, None)
            self._recorder.finalize()

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

        event_str = trace_str(event)

        record = FunctionRecord(
            self._index, event_str, function, frame.f_lineno,
            frame.f_code.co_filename)

        self._recorder.record(record)

        self._index += 1
        return 0
