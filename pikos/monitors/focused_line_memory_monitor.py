# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/focused_line_memory_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from pikos.monitors.line_memory_monitor import LineMemoryMonitor
from pikos.monitors.focused_line_mixin import FocusedLineMixin


class FocusedLineMemoryMonitor(FocusedLineMixin, LineMemoryMonitor):
    """ Record process memory on python function events.

    The class hooks on the settrace function to receive trace events and
    record the current process memory when a line of code is about to be
    executed. The events are recorded only when the interpreter is working
    inside the functions that are provided in the `functions` attribute.

    """
