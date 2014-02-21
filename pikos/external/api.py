# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: external/api.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
__all__ = [
    'PythonCProfiler',
    'YappiProfiler',
    'LineProfiler',
    'yappi_profile',
    'line_profile'
]

from pikos.external.python_cprofiler import PythonCProfiler
from pikos.external.yappi_profiler import YappiProfiler
from pikos.external.line_profiler import LineProfiler


def yappi_profile(buildins=None):
    """ Factory function that returns a yappi monitor.

    """
    return YappiProfiler(buildins)


def line_profile(*args, **kwrds):
    """ Factory function that returns a line profiler.

    Please refer to
    `<http://packages.python.org/line_profiler/ for more information>_`
    for initialization options.

    """
    return LineProfiler(*args, **kwrds)
