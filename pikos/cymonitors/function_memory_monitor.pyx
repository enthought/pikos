# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: cymonitors/function_memory_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#----------------------------------------------------------------------------
from cpython.pystate cimport (
    PyTrace_CALL, PyTrace_EXCEPTION, PyTrace_RETURN,  Py_tracefunc,
    PyTrace_C_CALL, PyTrace_C_EXCEPTION, PyTrace_C_RETURN)

from .function_monitor cimport FunctionMonitor
from .pytrace cimport PyEval_SetProfile, PyFrameObject

import os
import psutil

from pikos.monitors.records import FunctionMemoryRecord


cdef class FunctionMemoryMonitor(FunctionMonitor):
    """ Record process memory on python function events.

    The class hooks on the setprofile function to receive function events and
    record the current process memory when they happen.

    """

    def __init__(self, recorder, record_type=None):
        """ Constructor

        Parameters
        ----------
        recorder : Recorder
            The recorder inctance to use.

        record_type :
            The record type to use. Default is to use a FunctionRecord.

        """
        if record_type is None:
            record_type = FunctionMemoryRecord
        super(FunctionMemoryMonitor, self).__init__(recorder, record_type)
        self._process = None

    def enable(self):
        """ Enable the monitor.

        The first time the method is called (the context is entered) it will
        set the setprofile hooks and initialize the recorder.

        """
        if self._call_tracker('ping'):
            self._process = psutil.Process(os.getpid())
            self._recorder.prepare(self.record_type)
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

    cdef object _gather_info(
            self, PyFrameObject *_frame, int event, object arg):
        """ Record the current info.

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
        return record
