# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/focused_function_mixin.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from pikos.monitors.focused_monitor_mixin import FocusedMonitorMixin
from pikos._internal.keep_track import KeepTrack


class FocusedFunctionMixin(FocusedMonitorMixin):
    """ Mixing class to support recording python function events in a
    `focused` way.

    The method is used along a function event based monitor. It mainly
    overrides the on_function_event method to only record events when the
    interpreter is working inside the predefined functions.

    Public
    ------
    functions : FunctionSet
        A set of function or method objects inside which recording will
        take place.

    Private
    -------
    _code_trackers : dictionary
        A dictionary of KeepTrack instances associated with the code object
        of each function in `functions`. It is used to keep track and check
        that we are inside the execution of one these functions when we
        record data.

    """

    def __init__(self, *arguments, **keywords):
        """ Initialize the monitoring class.

        Parameters
        ----------
        *arguments : list
            The list of arguments required by the base monitor. They will
            be passed on the super class of the mixing

        **keywords : dict
            Dictionary of keyword arguments. The `functions` keyword if
            defined should be a list of function or method objects inside
            which recording will take place.

        """
        super(FocusedFunctionMixin, self).__init__(*arguments, **keywords)
        self._code_trackers = {}

    def on_function_event(self, frame, event, arg):
        """ Record the current function event only when we are inside one
        of the provided functions.

        """
        code = frame.f_code
        event_method = super(FocusedFunctionMixin, self).on_function_event
        if code in self.functions:
            tracker = self._code_trackers.setdefault(code, KeepTrack())
            if event == 'call':
                tracker('ping')
            else:
                tracker('pong')
            event_method(frame, event, arg)
            if not tracker:
                del self._code_trackers[code]
        elif any(self._code_trackers.itervalues()):
            event_method(frame, event, arg)
