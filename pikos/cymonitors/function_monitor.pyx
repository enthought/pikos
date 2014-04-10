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

from pikos._internal.keep_track import KeepTrack
from pikos.monitors.function_monitor import FunctionRecord


cdef class FunctionMonitor(Monitor):
    """ A Cython based monitor for function events.
    
    Private
    -------
    _recorder : Recorder
        reference to the recorder instance used by this monitor.
    
    """

    cdef public object _recorder
    cdef int _index
    cdef object _call_tracker
    cdef object record_type

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
        if record_type is None:
            self.record_type = FunctionRecord
        else:
            self.record_type = record_type

    def enable(self):
        """ Enable the monitor.

        The first time the method is called (the context is entered) it will
        set the setprofile hooks and initialize the recorder.

        """
        if self._call_tracker('ping'):
            self._recorder.prepare(self.record_type)
            if self.record_type == tuple:
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

        record = self.record_type(
            self._index, event_str, function, frame.f_lineno,
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

        record = (
            self._index, event_str, function, frame.f_lineno,
            frame.f_code.co_filename)

        self._recorder.record(record)

        self._index += 1
        return 0
