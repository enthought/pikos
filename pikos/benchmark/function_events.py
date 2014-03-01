# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: benchmark/monitors.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
""" Profile the python profile functions.

The benchmark runs the various pure python `set profile` methods by
simulating the fake calls.

"""
import cProfile
import inspect
import timeit

from line_profiler import LineProfiler

from pikos.monitors.function_monitor import FunctionRecord
from pikos.benchmark.record_counter import RecordCounter


class DummyFunctionMonitor(object):

    def __init__(self):
        self._index = 0
        self._recorder = RecordCounter()

    def original_method(self, frame, event, arg):
        filename, lineno, function, _, _ = \
            inspect.getframeinfo(frame, context=0)
        if event.startswith('c_'):
            function = arg.__name__
        record = FunctionRecord(self._index, event,
                                 function, lineno, filename)
        self._recorder.record(record)
        self._index += 1

    def step_one(self, frame, event, arg):
        lineno = frame.f_lineno
        code = frame.f_code
        filename = code.co_filename
        if event.startswith('c_'):
            function = arg.__name__
        else:
            function = code.co_name
        record = FunctionRecord(self._index, event,
                                function, lineno, filename)
        self._recorder.record(record)
        self._index += 1

    def step_two(self, frame, event, arg):
        lineno = frame.f_lineno
        code = frame.f_code
        filename = code.co_filename
        if 'c_' == event[:2]:
            function = arg.__name__
        else:
            function = code.co_name
        record = FunctionRecord(
            self._index, event, function, lineno, filename)
        self._recorder.record(record)
        self._index += 1

    def step_three(self, frame, event, arg):
        code = frame.f_code
        if 'c_' == event[:2]:
            record = FunctionRecord(
                self._index, event, arg.__name__,
                frame.f_lineno, code.co_filename)
        else:
            record = FunctionRecord(
                self._index, event, code.co_name,
                frame.f_lineno, code.co_filename)
        self._recorder.record(record)
        self._index += 1

    def step_four(self, frame, event, arg):
        if 'c_' == event[:2]:
            record = FunctionRecord(
                self._index, event, arg.__name__,
                frame.f_lineno, frame.f_code.co_filename)
        else:
            code = frame.f_code
            record = FunctionRecord(
                self._index, event, code.co_name,
                frame.f_lineno, code.co_filename)
        self._recorder.record(record)
        self._index += 1


def function_profile_monitor(method):
    frame = inspect.currentframe()
    for i in range(10000):
        method(frame, 'call', method)
    for i in range(10000):
        method(frame, 'return', method)
    for i in range(10000):
        method(frame, 'exception', method)
    for i in range(10000):
        method(frame, 'c_call', method)
    for i in range(10000):
        method(frame, 'c_return', method)
    for i in range(10000):
        method(frame, 'c_exception', method)


def main():
    profiler = cProfile.Profile()
    monitor = DummyFunctionMonitor()
    profiler.enable()
    function_profile_monitor(monitor.original_method)
    function_profile_monitor(monitor.step_one)
    function_profile_monitor(monitor.step_two)
    function_profile_monitor(monitor.step_three)
    function_profile_monitor(monitor.step_four)
    profiler.disable()
    profiler.dump_stats('function_event.stats')
    line_profiler = LineProfiler(monitor.step_four)
    line_profiler.enable()
    function_profile_monitor(monitor.step_four)
    line_profiler.disable()
    line_profiler.dump_stats('function_event.line_stats')
    line_profiler.print_stats()

    print timeit.timeit(
        lambda: function_profile_monitor(monitor.original_method), number=5)
    print timeit.timeit(lambda: function_profile_monitor(monitor.step_one), number=5)
    print timeit.timeit(lambda: function_profile_monitor(monitor.step_two), number=5)
    print timeit.timeit(lambda: function_profile_monitor(monitor.step_three), number=5)
    print timeit.timeit(lambda: function_profile_monitor(monitor.step_four), number=5)


if __name__ == '__main__':
    main()
