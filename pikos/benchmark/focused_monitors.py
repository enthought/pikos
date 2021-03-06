# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: benchmark/focused_monitors.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
""" Estimate the overhead cost of using a focused monitor.

The benchmark runs the pystones benchmark under each monitor and calculates
the overhead.

"""

from test import pystone

from pikos.benchmark.record_counter import RecordCounter


def pymonitors():
    """ Pure python monitors """
    from pikos.monitors.api import (
        FocusedFunctionMonitor, FocusedLineMonitor,
        FocusedFunctionMemoryMonitor, FocusedLineMemoryMonitor)
    return {
        'FocusedFunctionMonitor': FocusedFunctionMonitor,
        'FocusedLineMonitor': FocusedLineMonitor,
        'FocusedFunctionMemoryMonitor': FocusedFunctionMemoryMonitor,
        'FocusedLineMemoryMonitor': FocusedLineMemoryMonitor}


def cymonitors():
    """ Cython monitors """
    from pikos.cymonitors.api import FocusedFunctionMonitor
    return {
        'FocusedCFunctionMonitor': FocusedFunctionMonitor}


def run(monitors, loops, record_type=None):
    """ Time the monitors overhead using pystones.

    Parameter
    ---------
    monitors : list
        The list of monitors to time.

    loops : int
        The number of loops to run pystones.

    record_type : object
        The type of record to use.

    """
    header = (
        "Overhead time | Relative overhead | "
        "{:^10} | {:^{length}}".format(
            'Records', 'Name',
            length=max(len(key) for key in monitors) - 4))
    line = ('{time:>13} | {relative:>17} | {records:>10} | {name}')
    print header
    print len(header) * '-'
    expected_time, _ = pystone.pystones(loops)
    functions = [
        getattr(pystone, 'Proc{}'.format(index)) for index in range(4, 7)]
    for name, monitor in monitors.iteritems():
        recorder = RecordCounter()
        with monitor(
                functions=functions,
                recorder=recorder,
                record_type=record_type):
            time, _ = pystone.pystones(loops)
        print line.format(
            name=name,
            time='{:2.2f}'.format(time - expected_time),
            relative='{:.2%}'.format((time - expected_time) / expected_time),
            records='{:10d}'.format(recorder.records))


def main(monitors, loops=5000):
        print 'With default record types'
        run(monitors, loops)
        print
        print 'Using tuples as records'
        run(monitors, loops, record_type=tuple)


if __name__ == '__main__':
    monitors = pymonitors()
    monitors.update(cymonitors())
    main(monitors)
