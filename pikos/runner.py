# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/line_memory_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import argparse
import os
import sys

from pikos.monitors.api import (FunctionMonitor, LineMonitor,
                                                     FunctionMemoryMonitor,
                                                     LineMemoryMonitor)
from pikos.recorders.api import TextStreamRecorder

MONITORS = {'functions': FunctionMonitor,
            'lines': LineMonitor,
            'function_memory': FunctionMemoryMonitor,
            'line_memory': LineMemoryMonitor}

def run_code_under_monitor(script, monitor):
    """Compile the file and run inside the monitor context.

    Parameters
    ----------
    filename : str
       The filename of the script to run.

    monitor : object
       The monitor (i.e. context manager object) to use.

    """

    sys.path.insert(0, os.path.dirname(script))
    with open(script, 'rb') as handle:
        code = compile(handle.read(), script, 'exec')

    globs = {
        '__file__': script,
        '__name__': '__main__',
        '__package__': None}

    with monitor:
        exec code in globs, None



def main():
    description = "Execute the python script inside the pikos monitor context."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('monitor', choices=MONITORS.keys(),
                                       help='The monitor to use')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'),
                                        help='Output results to a file')
    parser.add_argument('--buffered', action='store_true',
                                        help='Use a buffered stream.')
    parser.add_argument('script', help='The script to run')
    args = parser.parse_args()

    stream = args.output if  args.output is not None else sys.stdout
    recorder = TextStreamRecorder(stream, auto_flush=(not args.buffered), formated=True)
    monitor = MONITORS[args.monitor](recorder=recorder)
    run_code_under_monitor(args.script, monitor)

if __name__ == '__main__':
    main()
