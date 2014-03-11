# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/focused_line_mixin.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import inspect

from pikos.monitors.focused_monitor_mixin import FocusedMonitorMixin


class FocusedLineMixin(FocusedMonitorMixin):
    """ Mixing class to support recording python line events in a `focused`
     way.

    The method is used along a line event based monitor. It mainly
    overrides the on_only_event method to only record events when the
    interpreter is working inside the predefined functions.

    Public
    ------
    functions : FunctionSet
        A set of function or method objects inside which recording will
        take place.

    """

    def on_line_event(self, frame, why, arg):
        """ Record the current function event only when we are inside one
        of the provided functions.

        """
        code = frame.f_code
        if code in self.functions:
            event_method = super(FocusedLineMixin, self).on_line_event
            event_method(frame, why, arg)
        return self.on_line_event

    def on_line_event_using_tuple(self, frame, why, arg):
        """ Record the current function event only when we are inside one
        of the provided functions.

        """
        code = frame.f_code
        if code in self.functions:
            event_method = super(
                FocusedLineMixin, self).on_line_event_using_tuple
            event_method(frame, why, arg)
        return self.on_line_event_using_tuple
