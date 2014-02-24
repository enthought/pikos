# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: benchmark/function_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from test import pystone

from pikos.monitors.api import *
from pikos.benchmark.record_counter import RecordCounter

monitors = {
    # Pure python monitors
    'FunctionMonitor': FunctionMonitor,
    'LineMonitor': LineMonitor,
    'FunctionMemoryMonitor': FunctionMemoryMonitor,
    'LineMemoryMonitor': LineMemoryMonitor,
}


def main(monitors, loops=500):

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
    main(monitors)







