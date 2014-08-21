# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: cymonitors/line_memory_monitor.pxd
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#----------------------------------------------------------------------------
from .line_monitor cimport LineMonitor


cdef class LineMemoryMonitor(LineMonitor):
    cdef object process
