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
import importlib
import os
import sys
import warnings

from pikos.api import (
    monitor_functions, monitor_lines, memory_on_functions, memory_on_lines,
    textfile, screen, csvfile)

MONITORS = {'functions': monitor_functions,
            'lines': monitor_lines,
            'function_memory': memory_on_functions,
            'line_memory': memory_on_lines}


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

    def executor():
        exec code in globs, None

    monitor(executor)()


def get_function(function_path):
    """ find and import a function dynamically.

    Parameters
    ----------
    function_path : string
        A string with the path to the function. The expected format is:

            - `<function>`
            - `<packages>.<module>.<function>`
            - `<packages>.<module>.<class>.<method>`


    """
    try:
        return importlib.import_module(function_path)
    except ImportError:
        components = function_path.split('.')
        try:
            module = importlib.import_module('.'.join(components[:-1]))
        except ImportError:
            module = importlib.import_module('.'.join(components[:-2]))
            class_object = getattr(module, components[-2])
            return getattr(class_object, components[-1])
        else:
            return getattr(module, components[-1])


def get_focused_on(script, focused_on):
    """ .

    Parameters
    ----------
    script : string
        The path of the script.

    focused_on : string
        The string of comma separate method paths to retrieve the function
        objects for.

    """
    if focused_on is not None:
        functions = []
        for item in focused_on.split(','):
            cleaned_item = item.strip()
            try:
                function = get_function(cleaned_item)
            except (ImportError, ValueError):
                module = os.path.splitext(
                    os.path.basename(script))[0]
                try:
                    function = get_function('.'.join((module, cleaned_item)))
                except (ImportError, ValueError):
                    raise ValueError(
                        'Cannot find function: {0}'.format(cleaned_item))
            functions.append(function)
    else:
        functions = None
    return functions


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
    parser.add_argument('--recording', choices=['screen', 'text', 'csv'],
                        help='Select the type of recording to use.',
                        default='screen'),
    parser.add_argument('--focused-on', help='Provide the module path(s) of '
                        'the method where recording will be focused. '
                        'Comma separated list of importable functions',
                        default=None),
    parser.add_argument('script', help='The script to run.')
    args = parser.parse_args()

    stream = args.output if args.output is not None else sys.stdout

    if args.recording == 'text':
        recorder = textfile()
    elif args.recording == 'csv':
        if not args.buffered:
            msg = ('Unbuffered output is not supported for csv recording.'
                   'The default options for the CSVWriter will be used.')
            warnings.warn(msg)
        recorder = csvfile()
    else:
        recorder = screen()

    script = args.script
    sys.path.insert(0, os.path.dirname(script))
    focus_on = get_focused_on(script, focused_on=args.focused_on)
    monitor = MONITORS[args.monitor](recorder=recorder, focus_on=focus_on)
    run_code_under_monitor(args.script, monitor)


if __name__ == '__main__':
    main()
