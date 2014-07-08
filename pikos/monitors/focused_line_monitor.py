# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/focused_line_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from pikos.monitors.line_monitor import LineMonitor
from pikos.monitors.focused_line_mixin import FocusedLineMixin


class FocusedLineMonitor(FocusedLineMixin, LineMonitor):
    """ Record python line events.

    The class hooks on the settrace function to receive trace events and
    record when a line of code is about to be executed. The events are
    recorded only when the interpreter is working inside the functions that
    are provided in the `functions` attribute.

    """
