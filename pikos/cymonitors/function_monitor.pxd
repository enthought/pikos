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
    cdef public object record_type
    cdef object _call_tracker
    cdef int _index
    cdef bint _use_tuple

    cdef int on_function_event(
        self, PyFrameObject *_frame, int event, object arg) except -1
    cdef object _gather_info(
        self, PyFrameObject *_frame, int event, object arg)
