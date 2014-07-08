#-*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/function_memory_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import os

import psutil

from pikos.monitors.function_monitor import FunctionMonitor
from pikos.monitors.records import FunctionMemoryRecord


class FunctionMemoryMonitor(FunctionMonitor):
    """ Record process memory on python function events.

    The class hooks on the setprofile function to receive function events and
    record the current process memory when they happen.

    Private
    -------
    _recorder : object
        A recorder object that implementes the
        :class:`~pikos.recorder.AbstractRecorder` interface.

    _profiler : object
        An instance of the
        :class:`~pikos._internal.profiler_functions.ProfilerFunctions` utility
        class that is used to set and unset the setprofile function as required
        by the monitor.

    _index : int
        The current zero based record index. Each function event will increase
        the index by one.

    _call_tracker : object
        An instance of the :class:`~pikos._internal.keep_track` utility class
        to keep track of recursive calls to the monitor's :meth:`__enter__` and
        :meth:`__exit__` methods.

    _process : object
        An instanse of :class:`psutil.Process` for the current process, used to
        get memory information in a platform independent way.

    _record_type : object
        A class object to be used for records. Default is
        :class:`~pikos.monitors.records.FunctionMemoryMonitor`

    _record_type: class object
        A class object to be used for records. Default is
        :class:`~pikos.monitors.records.FunctionMemoryMonitor`

    """

    def __init__(self, recorder, record_type=None):
        """ Initialize the monitoring class.

        Parameters
        ----------
        recorder : object
            A subclass of :class:`~pikos.recorders.AbstractRecorder` or a class
            that implements the same interface to handle the values to be
            logged.

        record_type: class object
            A class object to be used for records. Default is
            :class:`~pikos.monitors.records.FunctionMemoryMonitor`

        """
        if record_type is None:
            record_type = FunctionMemoryRecord
        super(FunctionMemoryMonitor, self).__init__(recorder, record_type)
        self._process = None

    def enable(self):
        """ Enable the monitor.

        The first time the method is called (the context is entered) it will
        initialize the Process class, set the setprofile hooks and initialize
        the recorder.

        """
        if self._call_tracker('ping'):
            self._process = psutil.Process(os.getpid())
            self._recorder.prepare(self._record_type)
            self._profiler.replace(self.on_function_event)

    def disable(self):
        """ Disable the monitor.

        The last time the method is called (the context is exited) it will
        unset the setprofile hooks and finalize the recorder and set
        :attr:`_process` to None.

        """
        if self._call_tracker('pong'):
            self._profiler.recover()
            self._recorder.finalize()
            self._process = None

    def _gather_info(self, frame, event, arg):
        """ Gather information for the record.

        """
        rss, vms = self._process.memory_info()
        if '_' == event[1]:
            return (
                self._index, event, arg.__name__, rss, vms,
                frame.f_lineno, frame.f_code.co_filename)
        else:
            code = frame.f_code
            return (
                self._index, event, code.co_name, rss, vms,
                frame.f_lineno, code.co_filename)
