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

from pikos.monitors.function_monitor import FunctionMonitor
from pikos.benchmark.record_counter import RecordCounter


def function_profile_monitor(monitor_factory, filename):
    recorder = RecordCounter()
    monitor = monitor_factory(recorder=recorder)
    profiler = cProfile.Profile()
    frame = inspect.currentframe()
    profiler.enable()
    for i in range(10000):
        monitor.on_function_event(frame, 'call', None)
    profiler.disable()
    profiler.dump_stats(filename)


def main():
    function_profile_monitor(FunctionMonitor, 'function_monitor_call')

if __name__ == '__main__':
    main()
