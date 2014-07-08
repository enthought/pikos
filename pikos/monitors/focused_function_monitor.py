# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/focused_function_monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from __future__ import absolute_import

from pikos.monitors.function_monitor import FunctionMonitor
from pikos.monitors.focused_function_mixin import FocusedFunctionMixin


class FocusedFunctionMonitor(FocusedFunctionMixin, FunctionMonitor):
    """ Record python function events.

    The class hooks on the setprofile function to receive function events and
    record them if they take place inside the provided functions.

    """
