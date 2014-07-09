# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/api.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#----------------------------------------------------------------------------
__all__ = [
    'FunctionMonitor',
    'FunctionMemoryMonitor',
    'LineMemoryMonitor',
    'LineMonitor',
    'FocusedFunctionMemoryMonitor',
    'FocusedLineMonitor',
    'FocusedLineMemoryMonitor',
    'FocusedFunctionMonitor',
    'MonitorAttach',
    'Monitor'
]

from pikos.monitors.function_monitor import FunctionMonitor
from pikos.monitors.line_monitor import LineMonitor
from pikos.monitors.focused_function_monitor import FocusedFunctionMonitor
from pikos.monitors.focused_line_monitor import FocusedLineMonitor
from pikos._internal.monitor_attach import MonitorAttach
from pikos.monitors.monitor import Monitor

try:
    import psutil
except ImportError:
    import warnings
    warnings.warn('Could not import psutil. Memory monitors are not available')
else:
    from pikos.monitors.function_memory_monitor import FunctionMemoryMonitor
    from pikos.monitors.line_memory_monitor import LineMemoryMonitor
    from pikos.monitors.focused_function_memory_monitor import \
        FocusedFunctionMemoryMonitor
    from pikos.monitors.focused_line_memory_monitor import \
        FocusedLineMemoryMonitor
