# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/line_memory_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from __future__ import absolute_import
import inspect
import os

import psutil

from pikos.monitors.line_monitor import LineMonitor
from pikos.monitors.records import LineMemoryRecord


class LineMemoryMonitor(LineMonitor):
    """ Record process memory on python line events.

    The class hooks on the settrace function to receive trace events and
    record the current process memory when a line of code is about to be
    executed.

    Private
    -------
    _recorder : object
        A recorder object that implementes the
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
        to keep track of recursive calls to the monitor's :meth:`__enter__`
        and :meth:`__exit__` methods.

    _process : object
       An instanse of :class:`psutil.Process` for the current process, used to
       get memory information in a platform independent way.

    _record_type: class object
        A class object to be used for records. Default is
        :class:`~pikos.monitors.records.LineMemoryMonitor`

    """

    def __init__(self, recorder, record_type=None):
        """ Initialize the monitoring class.

        Parameters
        ----------
        recorder : object
            A subclass of :class:`~pikos.recorders.AbstractRecorder` or a
            class that implements the same interface to handle the values
            to be recorded.

        record_type: class object
            A class object to be used for records. Default is
            :class:`~pikos.monitors.records.LineMemoryMonitor`

        """
        if record_type is None:
            record_type = LineMemoryRecord
        super(LineMemoryMonitor, self).__init__(recorder, record_type)
        self._process = None

    def enable(self):
        """ Enable the monitor.

        The first time the method is called (the context is entered) it will
        initialize the Process class, set the settrace hooks and initialize
        the recorder.

        """
        if self._call_tracker('ping'):
            self._process = psutil.Process(os.getpid())
            self._recorder.prepare(self._record_type)
            self._tracer.replace(self.on_line_event)

    def disable(self):
        """ Disable the monitor.

        The last time the method is called (the context is exited) it will
        unset the settrace hooks and finalize the recorder and set
        :attr:`_process` to None.

        """
        if self._call_tracker('pong'):
            self._tracer.recover()
            self._recorder.finalize()
            self._process = None

    def gather_info(self, frame):
        """ Gather memory information for the line.
        """
        rss, vms = self._process.memory_info()
        filename, lineno, function, line, _ = \
            inspect.getframeinfo(frame, context=1)
        if line is None:
            line = ['<compiled string>']
        return (
            self._index, function, lineno, rss, vms, line[0],
            filename)
