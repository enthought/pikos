#-*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/virtual_function_memory_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from __future__ import absolute_import
from collections import namedtuple

from win32api import GlobalMemoryStatusEx

from pikos._internal.profile_function_manager import ProfileFunctionManager
from pikos._internal.keep_track import KeepTrack
from pikos.monitors.function_monitor import FunctionMonitor
from pikos.monitors.monitor_attach import MonitorAttach


FUNCTION_VIRTUAL_BYTES_MEMORY_RECORD = (
    'index', 'type', 'function', 'virtual_bytes', 'lineNo', 'filename')
FUNCTION_VIRTUAL_BYTES_MEMORY_TEMPLATE = (
    u'{:>8} | {:<11} | {:<40} | {:>15} | {:>6} | {}')


class FunctionVirtualBytesMemoryRecord(
        namedtuple(
            'FunctionVirtualBytesMemoryRecord',
            FUNCTION_VIRTUAL_BYTES_MEMORY_RECORD)):

    __slots__ = ()

    header = FUNCTION_VIRTUAL_BYTES_MEMORY_TEMPLATE
    line = FUNCTION_VIRTUAL_BYTES_MEMORY_TEMPLATE


class FunctionVirtualBytesMemoryMonitor(FunctionMonitor):
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

    _record_type : object
        A class object to be used for records. Default is
        :class:`FunctionVirtualBytesMemoryRecord`

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
            :class:`FunctionVirtualBytesMemoryRecord`

        """
        if record_type is None:
            record_type = FunctionVirtualBytesMemoryRecord
        super(FunctionVirtualBytesMemoryMonitor, self).__init__(
            recorder=recorder, record_type=record_type)

    def on_function_event(self, frame, event, arg):
        """ Record the virtual bytes memory usage on function event.

        """
        result = GlobalMemoryStatusEx()
        virtual_bytes = result['TotalVirtual'] - result['AvailVirtual']
        if '_' == event[1]:
            record = self._record_type(
                self._index, event, arg.__name__,
                virtual_bytes, frame.f_lineno, frame.f_code.co_filename)
        else:
            code = frame.f_code
            record = self._record_type(
                self._index, event, code.co_name,
                virtual_bytes, frame.f_lineno, code.co_filename)
        self._record(record)
        self._index += 1

    def on_function_event_using_tuple(self, frame, event, arg):
        """ Record the virtual bytes memory usage on function, using tuples.

        """
        result = GlobalMemoryStatusEx()
        virtual_bytes = result['TotalVirtual'] - result['AvailVirtual']
        if '_' == event[1]:
            record = (
                self._index, event, arg.__name__,
                virtual_bytes, frame.f_lineno, frame.f_code.co_filename)
        else:
            code = frame.f_code
            record = (
                self._index, event, code.co_name,
                virtual_bytes, frame.f_lineno, code.co_filename)
        self._record(record)
        self._index += 1


def virtual_bytes_on_functions(recorder=None):
    """ Factory function that returns a virtual bytes function memory monitor.

    Parameters
    ----------
    recorder : AbstractRecorder
        The recorder to use and store the records. Default is outpout to screen.
    """
    if recorder is None:
        recorder = screen()
    monitor = FunctionVirtualBytesMemoryMonitor(recorder)
    return MonitorAttach(monitor)
