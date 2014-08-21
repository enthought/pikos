# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: cymonitors/line_memory_monitor.pyx
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#----------------------------------------------------------------------------
from cpython.pystate cimport Py_tracefunc, PyTrace_LINE

from .line_monitor cimport LineMonitor
from .pytrace cimport PyEval_SetTrace, PyFrameObject

import os
import psutil
from linecache import getline

from pikos.monitors.records import LineMemoryRecord


cdef class LineMemoryMonitor(LineMonitor):
    """ A Cython based monitor recording memory info on line events.

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
            record_type = LineMemoryRecord
        super(LineMemoryMonitor, self).__init__(recorder, record_type)
        self.process = None

    def enable(self):
        """ Enable the monitor.

        The first time the method is called (the context is entered) it will
        set the setprofile hooks and initialize the recorder.

        """
        if self.call_tracker('ping'):
            self.process = psutil.Process(os.getpid())
            self._recorder.prepare(self.record_type)
            PyEval_SetTrace(<Py_tracefunc>on_line_event, self)

    def disable(self):
        """ Disable the monitor.

        The last time the method is called (the context is exited) it will
        unset the setprofile hooks and finalize the recorder.

        """
        if self.call_tracker('pong'):
            PyEval_SetTrace(NULL, None)
            self._recorder.finalize()
            self.process = None

    cdef object gather_info(self, frame):
        """ Record the current info.

        """
        cdef:
            object record
            object code

        rss, vms = self.process.memory_info()
        code = frame.f_code
        filename = code.co_filename
        lineno = frame.f_lineno
        line = getline(filename, lineno)
        if len(line) == 0:
            line = '<compiled string>'
        record = (
            self.index, code.co_name, frame.f_lineno, rss, vms,
            line.rstrip(), filename)
        return record


cdef int on_line_event(
        LineMonitor monitor,
        PyFrameObject *_frame, int event, object arg) except -1:
    """ Tracer function to record the current line event.

    """
    cdef:
        object frame = <object>_frame

    # Make the frame right in case settrace(gettrace()) happens
    frame.f_trace = monitor
    if event == PyTrace_LINE:
        monitor.record_info(frame)
    return 0
