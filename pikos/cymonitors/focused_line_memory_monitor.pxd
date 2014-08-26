# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: cymonitors/focused_line_memory_monitor.pxd
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#----------------------------------------------------------------------------
from .line_memory_monitor cimport LineMemoryMonitor


cdef class FocusedLineMemoryMonitor(LineMemoryMonitor):
    cdef public object functions
