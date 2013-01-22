# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/focused_function_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from __future__ import absolute_import

from pikos.monitors.function_monitor import FunctionMonitor
from pikos.monitors.focused_function_mixin import FocusedFunctionMixin


class FocusedFunctionMonitor(FocusedFunctionMixin, FunctionMonitor):
    """ Record python function events.

    The class hooks on the setprofile function to receive function events and
    record them if they take place inside the provided functions.

    Public
    ------
    functions : FunctionSet
        A set of function or method objects inside which recording will
        take place.

    Private
    -------
    _recorder : object
        A recorder object that implementes the
        :class:`~pikos.recorder.AbstractRecorder` interface.

    _profiler : object
        An instance of the
        :class:`~pikos._internal.profiler_functions.ProfilerFunctions`
        utility class that is used to set and unset the setprofile function
        as required by the monitor.

    _index : int
        The current zero based record index. Each function event will increase
        the index by one.

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

    """
