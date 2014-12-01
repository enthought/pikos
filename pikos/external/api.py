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
]

import warnings

from pikos.external.python_cprofiler import PythonCProfiler

try:
    from pikos.external.yappi_profiler import YappiProfiler
except ImportError:
    warnings.warn(
        'YappiProfiler cannot be imported and will not be available')
else:
    def yappi_profile(buildins=None):
        """ Factory function that returns a yappi monitor.

        """
        return YappiProfiler(buildins)
    __all__.extend(['YappiProfiler', 'yappi_profile'])


try:
    from pikos.external.line_profiler import LineProfiler
except ImportError:
    warnings.warn(
        'LineProfile cannot be imported and will not be available')
else:
    def line_profile(*args, **kwrds):
        """ Factory function that returns a line profiler.

        Please refer to
        `<http://packages.python.org/line_profiler/ for more information>_`
        for initialization options.

        """
        return LineProfiler(*args, **kwrds)

    __all__.extend(['LineProfiler', 'line_profile'])
