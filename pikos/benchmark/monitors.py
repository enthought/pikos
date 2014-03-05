# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: benchmark/monitors.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
""" Estimate the overhead cost of using a monitor.

The benchmark runs the pystones benchmark under each monitor and calculates
the overhead.

"""

from test import pystone

from pikos.benchmark.record_counter import RecordCounter


def pymonitors():
    """ Pure python monitors """
    from pikos.monitors.api import (
        FunctionMonitor, LineMonitor,
        FunctionMemoryMonitor, LineMemoryMonitor)
    return {
    'FunctionMonitor': FunctionMonitor,
    'LineMonitor': LineMonitor,
    'FunctionMemoryMonitor': FunctionMemoryMonitor,
    'LineMemoryMonitor': LineMemoryMonitor}


def cymonitors():
    """ Cython monitors """
    from pikos.cmonitors.api import FunctionMonitor
    return {
    'CFunctionMonitor': FunctionMonitor}


def main(monitors, loops=1000):
    header = (
        "Overhead time | Relative overhead | "
        "{:^10} |  Per record  | {:^{length}}".format(
            'Records', 'Name',
            length=max(len(key) for key in monitors) - 4))
    line = ('{time:>13} | {relative:>17} | {records:>10} '
            '| {time_per_record:.6e} | {name}')
    print header
    print len(header) * '-'
    expected_time, _ = pystone.pystones(loops)
    for name, monitor in monitors.iteritems():
        recorder = RecordCounter()
        with monitor(recorder=recorder):
            time, _ = pystone.pystones(loops)
        time_per_record = (time - expected_time) / recorder.records
        print line.format(
            name=name,
            time='{:2.2f}'.format(time - expected_time),
            relative='{:.2%}'.format((time - expected_time) / expected_time),
            time_per_record=time_per_record,
            records='{:10d}'.format(recorder.records))


if __name__ == '__main__':
    monitors = pymonitors()
    monitors.update(cymonitors())
    main(monitors)
