# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: cymonitors/focused_line_monitor.pxd
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#----------------------------------------------------------------------------
from .line_monitor cimport LineMonitor

cdef class FocusedLineMonitor(LineMonitor):
    cdef public object functions
