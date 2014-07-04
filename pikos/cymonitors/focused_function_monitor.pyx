# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: cymonitors/focused_function_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#----------------------------------------------------------------------------
from cpython.pystate cimport PyTrace_CALL

from .function_monitor cimport FunctionMonitor
from .pytrace cimport PyFrameObject

from pikos._internal.keep_track import KeepTrack
from pikos._internal.function_set import FunctionSet
from pikos.monitors.attach_decorators import advanced_attach


cdef class FocusedFunctionMonitor(FunctionMonitor):
    """ A Cython based monitor for recording function events when inside a set
    of functions.

    Public
    ------
    functions : FunctionSet
        A set of function or method objects inside which recording will
        take place.

    Private
    -------

    _call_tracker : object
        An instance of the :class:`~pikos._internal.keep_track` utility class
        to keep track of recursive calls to the monitor's :meth:`__enter__`
         and
        :meth:`__exit__` methods.

    _code_trackers : dictionary
        A dictionary of KeepTrack instances associated with the code object
        of each function in `functions`. It is used to keep track and check
        that we are inside the execution of one these functions when we
        record data.

    _index : int
        The current zero based record index. Each function event will increase
        the index by one.

    _record_type: class object
        A class object to be used for records. Default is
        :class:`~pikos.monitors.records.FunctionMonitor`

    _recorder : object
        A recorder object that implementes the
        :class:`~pikos.recorder.AbstractRecorder` interface.

    """

    cdef public object functions
    cdef public dict _code_trackers

    def __init__(self, functions, recorder, record_type=None):
        """ Constructor

        Parameters
        ----------
        recorder : Recorder
            The recorder inctance to use.

        record_type :
            The record type to use. Default is to use a FunctionRecord.

        """
        super(FocusedFunctionMonitor, self).__init__(recorder, record_type)
        self.functions = FunctionSet(functions)
        self._code_trackers = {}

    cdef int on_function_event(
            self, PyFrameObject *_frame, int event, object arg) except -1:
        """ Record the function event if we are inside one of the functions.

        """
        if self._tracker_check(_frame, event):
            FunctionMonitor.on_function_event(self, _frame, event, arg)

    cdef int on_function_event_tuple(
            self, PyFrameObject *_frame, int event, object arg) except -1:
        """ Record the function event if we are inside one of the functions.

        .. note::

          Method optimized for tuples as records.

        """
        if self._tracker_check(_frame, event):
            FunctionMonitor.on_function_event_tuple(self, _frame, event, arg)

    cdef bint _tracker_check(self, PyFrameObject *_frame, int event):
        """ Check if any function tracker is currently active.

        """
        cdef:
            object frame = <object>_frame
        code = frame.f_code
        if code in self.functions:
            tracker = self._code_trackers.setdefault(code, KeepTrack())
            if event == PyTrace_CALL:
                tracker('ping')
            else:
                tracker('pong')
            if not tracker:
                del self._code_trackers[code]
            return True
        return any(self._code_trackers.itervalues())

    # Override the default attach method to support arguments.
    attach = advanced_attach
