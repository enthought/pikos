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
    
    Each method implements a stage in the function event (i.e. set_profile)
    compatible function. 
    The current 
    
    """
    def __init__(self):
        self._index = 0
        self._recorder = RecordCounter()
        self.namedtuple_record = FunctionRecord
        self.tuple_record = lambda *x: x

    def original_method(self, frame, event, arg):
        """ The original method for the function event monitor.
        """
        filename, lineno, function, _, _ = \
            inspect.getframeinfo(frame, context=0)
        if event.startswith('c_'):
            function = arg.__name__
        record = FunctionRecord(self._index, event, function, lineno, filename)
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
        record = FunctionRecord(self._index, event, function, lineno, filename)
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
        """ Forth step -- do not create `code` variable on some events.

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
        """ Seventh step -- use a tuple instead of a lambda.
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

class CurrentFunctionContainer(object):
    """ Class holding the currently used function event method in pikos.
    
    """
    
    def __init__(self, recorder):
        self.current = FunctionMonitor(
            recorder, record_type=tuple).on_function_event


class SlotsFunctionContainer(object):
    """ A function container using slots for the class attributes.

    """
    __slots__ = ('index', '_recorder', 'record')

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


method_map = [
    ['step_one', 'step_two', 'step_three', 'step_four', 
     'step_five', 'step_six', 'step_seven'] : FunctionContainer,
    ['step_eight', 'step_nine']: SlotsFunctionContainer,
    ['current'] : CurrentFunctionContainer]



def function_runner(method_name, number=10000):
    """ Simulate calling the event function with the different event types.
    
    Parameters
    ----------
    method_name : string
        The name of the method to use.
    
    numbers : int
        The number of events to create for each event type.
        
    """
    for method_names, cls in method_map:
        if method_name in method_names:
            break
    else:
        raise ValueError('could not find method {0}'.format(method_name))

    monitor = cls()
    method = getattr(monitor, method_name)
    
    frame = inspect.currentframe()
    for i in range(events):
        method(frame, 'call', method)
    for i in range(events):
        method(frame, 'return', method)
    for i in range(events):
        method(frame, 'exception', method)
    for i in range(events):
        method(frame, 'c_call', method)
    for i in range(events):
        method(frame, 'c_return', method)
    for i in range(events):
        method(frame, 'c_exception', method)


def main():
    profiler = cProfile.Profile()

    profiler.enable()
    function_runner('original_method')
    function_runner('step_one)
    function_runner('step_two)
    function_runner('step_three)
    function_runner('step_four)
    function_runner('step_five)
    function_runner('step_six)
    function_runner('step_seven)
    function_runner('step_eight)
    function_runner('step_nine)
    function_runner('current')
    profiler.disable()

    profiler.dump_stats('function_event.stats')
    line_profiler = LineProfiler(monitor.step_nine)
    line_profiler.enable()
    function_runner('step_nine')
    line_profiler.disable()
    line_profiler.dump_stats('function_event.line_stats')
    line_profiler.print_stats()

    print 'Original', timeit.timeit(
        lambda: function_runner('original_method'), number=7)
    print 'One', timeit.timeit(
        lambda: function_runner('step_one'), number=7)
    print 'Two', timeit.timeit(
        lambda: function_runner('step_two'), number=7)
    print 'Three', timeit.timeit(
        lambda: function_runner('step_three'), number=7)
    print 'Four', timeit.timeit(
        lambda: function_runner('step_four'), number=7)
    print 'Five', timeit.timeit(
        lambda: function_runner('step_five'), number=7)
    print 'Six', timeit.timeit(
        lambda: function_runner('step_six'), number=7)
    print 'Seven', timeit.timeit(
        lambda: function_runner('step_seven'), number=7)
    print 'Eight', timeit.timeit(
        lambda: function_runner('step_eight'), number=7)
    print 'Nine', timeit.timeit(
        lambda: function_runner('step_nine'), number=7)
    print 'Current', timeit.timeit(
        lambda: function_runner('current'), number=7)


if __name__ == '__main__':
    main()
