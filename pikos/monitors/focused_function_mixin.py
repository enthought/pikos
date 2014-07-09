# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/focused_function_mixin.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from pikos._internal.keep_track import KeepTrack
from pikos._internal.function_set import FunctionSet
from pikos._internal.attach_decorators import advanced_attach


class FocusedFunctionMixin(object):
    """ Mixing class to support recording python function events `focused` on
    a set of functions.

    The method is used along a function event based monitor. It mainly
    overrides the on_function_event method to only record events when the
    interpreter is working inside one of predefined functions.

    Public
    ------
    functions : FunctionSet
        A set of function or method objects inside which recording will
        take place.

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
        functions = keywords.pop('functions', ())
        super(FocusedFunctionMixin, self).__init__(*arguments, **keywords)
        self.functions = FunctionSet(functions)
        self._code_trackers = {}

    def on_function_event(self, frame, event, arg):
        """ Record the function event if we are inside one of the functions.

        """
        if self._tracker_check(frame, event):
            super(FocusedFunctionMixin, self).on_function_event(
                frame, event, arg)

    def _tracker_check(self, frame, event):
        """ Check if any function tracker is currently active.

        """
        code = frame.f_code
        if code in self.functions:
            tracker = self._code_trackers.setdefault(code, KeepTrack())
            if event == 'call':
                tracker('ping')
            else:
                tracker('pong')
            if not tracker:
                del self._code_trackers[code]
            return True
        return any(self._code_trackers.itervalues())

    # Override the default attach method to support arguments.
    attach = advanced_attach
