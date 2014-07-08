# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/focused_function_memory_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from __future__ import absolute_import

from pikos.monitors.function_memory_monitor import FunctionMemoryMonitor
from pikos.monitors.focused_function_mixin import FocusedFunctionMixin


class FocusedFunctionMemoryMonitor(FocusedFunctionMixin,
                                   FunctionMemoryMonitor):
    """ Record process memory on python function events.

    The class hooks on the setprofile function to receive function events and
    record while inside the provided functions the current process memory
    when they happen.

    Public
    ------
    functions : FunctionSet
        A set of function or method objects inside which recording will
        take place.

    """
