# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: cymonitors/focused_line_memory_monitor.pyx
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#----------------------------------------------------------------------------
from .line_memory_monitor cimport LineMemoryMonitor

from pikos._internal.function_set import FunctionSet
from pikos._internal.attach_decorators import advanced_attach


cdef class FocusedLineMemoryMonitor(LineMemoryMonitor):
    """ A Cython based monitor for recording process memory on line events
    when inside a set of functions.

    Public
    ------
    functions : FunctionSet
        A set of function or method objects inside which recording will
        take place.

    """

    def __init__(self, functions, recorder, record_type=None):
        """ Constructor

        Parameters
        ----------
        recorder : Recorder
            The recorder inctance to use.

        record_type : type
            The record type to use. Default is to use a LineRecord.

        """
        super(FocusedLineMemoryMonitor, self).__init__(recorder, record_type)
        self.functions = FunctionSet(functions)

    cdef record_info(self, _frame):
        """ Record the current info.

        """
        cdef:
            object frame = <object>_frame

        code = frame.f_code
        if code in self.functions:
            LineMemoryMonitor.record_info(self, frame)

    # Override the default attach method to support arguments.
    attach = advanced_attach
