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
simulating the fake calls. The methods are named by increasing order of
optimization.

"""
import cProfile
import inspect
import timeit

from line_profiler import LineProfiler

from pikos.monitors.function_monitor import FunctionRecord, FunctionMonitor
from pikos.benchmark.record_counter import RecordCounter

cevent = '_'

class FunctionContainer(object):
    """ The event function container.
    """
    def __init__(self):
        self._index = 0
        self._recorder = RecordCounter()
        self.namedtuple_record = FunctionRecord
        self.tuple_record = lambda *x: x
        self.current = FunctionMonitor(
            self._recorder, record_type=tuple).on_function_event
        self.step_eight = SlotsMonitor(self._recorder).step_eight
        self.step_nine = SlotsMonitor(self._recorder).step_nine

    def original_method(self, frame, event, arg):
        """ The original method for the function event monitor.
        """
        filename, lineno, function, _, _ = \
            inspect.getframeinfo(frame, context=0)
        if event.startswith('c_'):
            function = arg.__name__
        record = FunctionRecord(self._index, event,
                                 function, lineno, filename)
        self._recorder.record(record)
        self._index += 1

    def step_one(self, frame, event, arg):
        """ First step -- remove the use of inspect.
        """
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
        """ Second step -- simplify check of c function related events.
        """
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
        """ Third step -- do not create the `function` variable.
        """
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
        """ Forth step -- do not create `code` variable when it is going to be
        used once.

        """
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

    def step_five(self, frame, event, arg):
        """ Fifth step -- store the record type on an instance attribute.

        .. note ::
            This a marginally slower than before but we need to support custom
            records.

        """
        if 'c_' == event[:2]:
            record = self.namedtuple_record(
                self._index, event, arg.__name__,
                frame.f_lineno, frame.f_code.co_filename)
        else:
            code = frame.f_code
            record = self.namedtuple_record(
                self._index, event, code.co_name,
                frame.f_lineno, code.co_filename)
        self._recorder.record(record)
        self._index += 1

    def step_six(self, frame, event, arg):
        """ Sixth step -- use a tuple creating lambda instead of a named tuple.
        """
        if 'c_' == event[:2]:
            record = self.tuple_record(
                self._index, event, arg.__name__,
                frame.f_lineno, frame.f_code.co_filename)
        else:
            code = frame.f_code
            record = self.tuple_record(
                self._index, event, code.co_name,
                frame.f_lineno, code.co_filename)
        self._recorder.record(record)
        self._index += 1

    def step_seven(self, frame, event, arg):
        """ Seventh step -- use a tuple instead of a lambda
        """
        if 'c_' == event[:2]:
            record = (
                self._index, event, arg.__name__,
                frame.f_lineno, frame.f_code.co_filename)
        else:
            code = frame.f_code
            record = (
                self._index, event, code.co_name,
                frame.f_lineno, code.co_filename)
        self._recorder.record(record)
        self._index += 1


class SlotsMonitor(object):

    def __init__(self, recorder):
        self.index = 0
        self._recorder = recorder
        self.record = recorder.record

    def step_eight(self, frame, event, arg):
        """ Eigthth step -- single char check for c events.
        """
        if '_' == event[1]:
            record = (
                self.index, event, arg.__name__,
                frame.f_lineno, frame.f_code.co_filename)
        else:
            code = frame.f_code
            record = (
                self.index, event, code.co_name,
                frame.f_lineno, code.co_filename)
        self._recorder.record(record)
        self.index += 1

    def step_nine(self, frame, event, arg):
        """ Nineth step -- store the record method into a private attribute.
        """
        if '_' == event[1]:
            record = (
                self.index, event, arg.__name__,
                frame.f_lineno, frame.f_code.co_filename)
        else:
            code = frame.f_code
            record = (
                self.index, event, code.co_name,
                frame.f_lineno, code.co_filename)
        self.record(record)
        self.index += 1


def function_runner(method):
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
    monitor = FunctionContainer()

    profiler.enable()
    function_runner(monitor.original_method)
    function_runner(monitor.step_one)
    function_runner(monitor.step_two)
    function_runner(monitor.step_three)
    function_runner(monitor.step_four)
    function_runner(monitor.step_five)
    function_runner(monitor.step_six)
    function_runner(monitor.step_seven)
    function_runner(monitor.step_eight)
    function_runner(monitor.step_nine)
    function_runner(monitor.current)
    profiler.disable()

    profiler.dump_stats('function_event.stats')
    line_profiler = LineProfiler(monitor.step_nine)
    line_profiler.enable()
    function_runner(monitor.step_nine)
    line_profiler.disable()
    line_profiler.dump_stats('function_event.line_stats')
    line_profiler.print_stats()

    print 'Original', timeit.timeit(
        lambda: function_runner(monitor.original_method), number=7)
    print 'One', timeit.timeit(
        lambda: function_runner(monitor.step_one), number=7)
    print 'Two', timeit.timeit(
        lambda: function_runner(monitor.step_two), number=7)
    print 'Three', timeit.timeit(
        lambda: function_runner(monitor.step_three), number=7)
    print 'Four', timeit.timeit(
        lambda: function_runner(monitor.step_four), number=7)
    print 'Five', timeit.timeit(
        lambda: function_runner(monitor.step_five), number=7)
    print 'Six', timeit.timeit(
        lambda: function_runner(monitor.step_six), number=7)
    print 'Seven', timeit.timeit(
        lambda: function_runner(monitor.step_seven), number=7)
    print 'Eight', timeit.timeit(
        lambda: function_runner(monitor.step_eight), number=7)
    print 'Nine', timeit.timeit(
        lambda: function_runner(monitor.step_nine), number=7)
    print 'Current', timeit.timeit(
        lambda: function_runner(monitor.current), number=7)


if __name__ == '__main__':
    main()
