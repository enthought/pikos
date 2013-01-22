# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/focused_line_memory_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from pikos.monitors.line_memory_monitor import LineMemoryMonitor
from pikos.monitors.focused_line_mixin import FocusedLineMixin


class FocusedLineMemoryMonitor(FocusedLineMixin, LineMemoryMonitor):
    """ Record process memory on python function events.

    The class hooks on the settrace function to receive trace events and
    record the current process memory when a line of code is about to be
    executed. The events are recorded only when the interpreter is working
    inside the functions that are provided in the `functions` attribute.

    Public
    ------
    functions : FunctionSet
        A set of function or method objects inside which recording will
        take place.

    Private
    -------
    _recorder : object
        A recorder object that implements the
        :class:`~pikos.recorder.AbstractRecorder` interface.

    _tracer : object
        An instance of the
        :class:`~pikos._internal.trace_functions.TraceFunctionManager` utility
        class that is used to set and unset the settrace function as required
        by the monitor.

    _index : int
        The current zero based record index. Each function event will increase
        the index by one.

    _call_tracker : object
        An instance of the :class:`~pikos._internal.keep_track` utility class
        to keep track  of recursive calls to the monitor's :meth:`__enter__`
        and :meth:`__exit__` methods.

    _process : object
        An instanse of :class:`psutil.Process` for the current process,
        used to get memory information in a platform independent way.

    _code_trackers: dict
        A dictionary of KeepTrack instances associated with the code object
        of each function in `functions`. It is used to keep track and check
        that we are inside the execution of one these functions when we
        record data.

    """
