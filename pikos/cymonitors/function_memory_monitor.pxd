# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: cymonitors/function_memory_monitor.pxd
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#----------------------------------------------------------------------------
from .function_monitor cimport FunctionMonitor


cdef class FunctionMemoryMonitor(FunctionMonitor):
    cdef object _process
