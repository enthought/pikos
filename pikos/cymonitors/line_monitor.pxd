# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: cymonitors/line_monitor.pxd
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#----------------------------------------------------------------------------
from .monitor cimport Monitor
from .pytrace cimport PyFrameObject

cdef class LineMonitor(Monitor):
    cdef public object _recorder
    cdef public object record_type
    cdef int index
    cdef object call_tracker
    cdef bint use_tuple
    cdef object record_info(self, frame)
    cdef object gather_info(self, frame)

cdef int on_line_event(
    LineMonitor monitor,
    PyFrameObject *_frame, int event, object arg) except -1
