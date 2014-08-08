# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: cymonitors/line_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#----------------------------------------------------------------------------
from cpython.pystate cimport Py_tracefunc, PyTrace_LINE

from .monitor cimport Monitor
from .pytrace cimport PyEval_SetTrace, PyFrameObject

from linecache import getline

from pikos._internal.keep_track import KeepTrack
from pikos.monitors.records import LineRecord


cdef class LineMonitor(Monitor):
    """ A Cython based monitor for line events.
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
        self._recorder = recorder
        self._call_tracker = KeepTrack()
        if record_type is None:
            self.record_type = LineRecord
        else:
            self.record_type = record_type
        self._use_tuple = self.record_type is tuple

    def enable(self):
        """ Enable the monitor.

        The first time the method is called (the context is entered) it will
        set the setprofile hooks and initialize the recorder.

        """
        if self._call_tracker('ping'):
            self._recorder.prepare(self.record_type)
            PyEval_SetTrace(<Py_tracefunc>on_line_event, self)

    def disable(self):
        """ Disable the monitor.

        The last time the method is called (the context is exited) it will
        unset the setprofile hooks and finalize the recorder.

        """
        if self._call_tracker('pong'):
            PyEval_SetTrace(NULL, None)
            self._recorder.finalize()

    def __call__(self, frame, why, arg):
        # We need to define a callable incase settrace(gettrace()) happens.
        # see http://nedbatchelder.com/text/trace-function.html for more info
        if why[0] == 'l':
            self._record_info(frame)
        return self

    cdef object _record_info(self, frame):
        """ Record the current info.

        """
        cdef:
            object record
            object code

        code = frame.f_code
        filename = code.co_filename
        lineno = frame.f_lineno
        line = getline(filename, lineno)
        if len(line) == 0:
            line = '<compiled string>'
        record = (
            self._index, code.co_name, frame.f_lineno, line.rstrip(),
            filename)
        if not self._use_tuple:
            record = self.record_type(*record)
        self._recorder.record(record)
        self._index += 1


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
        monitor._record_info(frame)
    return 0
