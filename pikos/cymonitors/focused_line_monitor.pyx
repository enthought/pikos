# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: cymonitors/focused_line_monitor.pyx
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#----------------------------------------------------------------------------
from .line_monitor cimport LineMonitor

from pikos._internal.function_set import FunctionSet
from pikos._internal.attach_decorators import advanced_attach


cdef class FocusedLineMonitor(LineMonitor):
    """ A Cython based monitor for recording line events when inside a set
    of functions.

    Public
    ------
    functions : FunctionSet
        A set of function or method objects inside which recording will
        take place.

    Private
    -------

    _record_type: class object
        A class object to be used for records. Default is
        :class:`~pikos.monitors.records.LineRecord`

    _recorder : object
        A recorder object that implementes the
        :class:`~pikos.recorder.AbstractRecorder` interface.

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
        super(FocusedLineMonitor, self).__init__(recorder, record_type)
        self.functions = FunctionSet(functions)

    cdef record_info(self, frame):
        """ Record the current info.

        """
        code = frame.f_code
        if code in self.functions:
            LineMonitor.record_info(self, frame)

    # Override the default attach method to support arguments.
    attach = advanced_attach
