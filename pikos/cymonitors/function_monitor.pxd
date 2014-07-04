# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: cmonitors/function_monitor.pxd
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#----------------------------------------------------------------------------
from .monitor cimport Monitor
from .pytrace cimport PyFrameObject

cdef class FunctionMonitor(Monitor):
    cdef public object _recorder
    cdef int _index
    cdef object _call_tracker
    cdef object record_type

    cdef int on_function_event(
        self, PyFrameObject *_frame, int event, object arg) except -1
    cdef int on_function_event_tuple(
        self, PyFrameObject *_frame, int event, object arg) except -1
