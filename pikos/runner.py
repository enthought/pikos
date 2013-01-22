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
import imp
import os
import sys
import warnings

from pikos.monitors.api import (FunctionMonitor, LineMonitor,
                                FunctionMemoryMonitor, LineMemoryMonitor,
                                FocusedFunctionMemoryMonitor,
                                FocusedLineMemoryMonitor, FocusedLineMonitor,
                                FocusedFunctionMonitor)
from pikos.recorders.api import TextStreamRecorder, CSVRecorder

MONITORS = {'functions': FunctionMonitor,
            'lines': LineMonitor,
            'function_memory': FunctionMemoryMonitor,
            'line_memory': LineMemoryMonitor}

FOCUSED_MONITORS = {'functions': FocusedFunctionMonitor,
                    'lines': FocusedLineMonitor,
                    'function_memory': FocusedFunctionMemoryMonitor,
                    'line_memory': FocusedLineMemoryMonitor}


def run_code_under_monitor(script, monitor):
    """Compile the file and run inside the monitor context.

    Parameters
    ----------
    script : str
       The filename of the script to run.

    monitor : object
       The monitor (i.e. context manager object) to use.

    """
    sys.path.insert(0, os.path.dirname(script))
    with open(script, 'rb') as handle:
        code = compile(handle.read(), script, 'exec')

    globs = {'__file__': script, '__name__': '__main__', '__package__': None}
    with monitor:
        exec code in globs, None


def get_function(function_path):
    """ find and import a function dynamically.

    Parameters
    ----------
    function_path : string
       a string with the path to the function. The expected format is::

                `<packages>.<module>.<function>`
           or::

                `<packages>.<module>.<class>.<method>`

    """
    if '.' not in function_path:
        raise ValueError('The module path format should be'
                         '<packages>.<module>.<function>'
                         'or <packages>.<module>.<class>.<method>')
    else:
        components = function_path.split('.')

    for index, component in enumerate(components):
        handle, pathname, description = imp.find_module(
            component,
            sys.path + ['./'])
        if description != imp.PKG_DIRECTORY:
            break
    else:
        raise RuntimeError('Could not find module {}'.format(function_path))

    remaining = len(components) - index - 1
    if remaining > 2:
        raise ValueError('The module path format should be'
                         '<packages>.<module>.<function>'
                         'or <packages>.<module>.<class>.<method>')
    try:
        module = imp.load_module('.'.join(components[:-1]),
                                 handle, pathname, description)
    finally:
        handle.close()

    if remaining == 1:
        return getattr(module, components[-1])
    elif remaining == 2:
        class_type = getattr(module, components[-2])
        return getattr(class_type, components[-1])
    else:
        raise RuntimeError('This option should never happen')


def main():
    description = "Execute the python script inside the pikos monitor " \
                  "context."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('monitor', choices=MONITORS.keys(),
                        help='The monitor to use')
    parser.add_argument('-o', '--output', type=argparse.FileType('wb'),
                        help='Output results to a file')
    parser.add_argument('--buffered', action='store_false',
                        help='Use a buffered stream.')
    parser.add_argument('--recording', choices=['text', 'csv'],
                        help='Select the type of recording to use.',
                        default='text'),
    parser.add_argument('--focused-on', help='Provide the module path(s) of '
                        'the method where recording will be focused. '
                        'Comma separated list of importable functions',
                        default=None),
    parser.add_argument('script', help='The script to run.')
    args = parser.parse_args()

    stream = args.output if args.output is not None else sys.stdout

    if args.recording == 'text':
        recorder = TextStreamRecorder(stream,
                                      auto_flush=(not args.buffered),
                                      formated=True)
    else:
        if not args.buffered:
            msg = ('Unbuffered output is not supported for csv recording.'
                   'The default options for the CSVWriter will be used.')
            warnings.warn(msg)
        recorder = CSVRecorder(stream)

    if args.focused_on is None:
        monitor = MONITORS[args.monitor](recorder=recorder)
    else:
        functions = []
        for item in args.focused_on.split(','):
            function = get_function(item)
            functions.append(function)
        monitor = FOCUSED_MONITORS[args.monitor](recorder=recorder,
                                                 functions=functions)
    run_code_under_monitor(args.script, monitor)

if __name__ == '__main__':
    main()
