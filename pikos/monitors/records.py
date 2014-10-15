# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/records.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from collections import namedtuple

FUNCTION_RECORD = ('index', 'type', 'function', 'lineNo', 'filename')
FUNCTION_RECORD_TEMPLATE = u'{:<8} {:<11} {:<30} {:<5} {}'

LINE_RECORD = ('index', 'function', 'lineNo', 'line', 'filename')
LINE_RECORD_TEMPLATE = u'{:<12} {:<50} {:<7} {} -- {}'

FUNCTION_MEMORY_RECORD = (
    'index', 'type', 'function', 'RSS', 'VMS', 'lineNo', 'filename')
FUNCTION_MEMORY_RECORD_TEMPLATE = (
    u'{:>8} | {:<11} | {:<12} | {:>15} | {:>15} | {:>6} | {}')
FUNCTION_MEMORY_HEADER_TEMPLATE = (
    u'{:<8} | {:<11} | {:<12} | {:<15} | {:<15} | {:>6} | {}')

LINE_MEMORY_RECORD = (
    'index', 'function', 'lineNo', 'RSS', 'VMS', 'line', 'filename')
LINE_MEMORY_RECORD_TEMPLATE = (
    u'{:<12} | {:<30} | {:<7} | {:>15} | {:>15} | {} {}')
LINE_MEMORY_HEADER_TEMPLATE = (
    u'{:^12} | {:^30} | {:^7} | {:^15} | {:^15} | {} {}')


class FunctionRecord(namedtuple('FunctionRecord', FUNCTION_RECORD)):
    """ The record tuple for function events.

    ========== ================================================
    Field      Description
    ========== ================================================
    `index`    The current index of the record.
    `type`     The type of the event (see Python trace method).
    `function` The name of the function.
    `lineNo`   The line number when the function is defined.
    `filename` The filename where the function is defined.
    ========== ================================================

    """

    __slots__ = ()

    header = FUNCTION_RECORD_TEMPLATE
    line = FUNCTION_RECORD_TEMPLATE


class LineRecord(namedtuple('LineRecord', LINE_RECORD)):
    """ The record for line trace events.

    ========== ================================================
    Field      Description
    ========== ================================================
    `index`    The current index of the record.
    `function` The name of the function.
    `lineNo`   The line number when the function is defined.
    `line`     The line that is going to be executed.
    `filename` The filename where the function is defined.
    ========== ================================================

    """

    __slots__ = ()

    header = LINE_RECORD_TEMPLATE
    line = LINE_RECORD_TEMPLATE


class FunctionMemoryRecord(
        namedtuple('FunctionMemoryRecord', FUNCTION_MEMORY_RECORD)):
    """ The record tuple for memory usage on function events.

    ========== ================================================
    Field      Description
    ========== ================================================
    `index`    The current index of the record.
    `type`     The type of the event (see Python trace method).
    `function` The name of the function.
    `RSS`      The resident memory counter.
    `VMS`      The virtual memory counter.
    `lineNo`   The line number when the function is defined.
    `filename` The filename where the function is defined.
    ========== ================================================

    """

    __slots__ = ()

    header = FUNCTION_MEMORY_HEADER_TEMPLATE
    line = FUNCTION_MEMORY_RECORD_TEMPLATE


class LineMemoryRecord(namedtuple('LineMemoryRecord', LINE_MEMORY_RECORD)):
    """ The record tuple for memory usage on line events.

    ========== ================================================
    Field      Description
    ========== ================================================
    `index`    The current index of the record.
    `function` The name of the function
    `RSS`      The resident memory counter.
    `VMS`      The virtual memory counter.
    `lineNo`   The line number when the function is defined.
    `filename` The filename where the function is defined.
    ========== ================================================

    """

    __slots__ = ()

    header = LINE_MEMORY_HEADER_TEMPLATE
    line = LINE_MEMORY_RECORD_TEMPLATE
