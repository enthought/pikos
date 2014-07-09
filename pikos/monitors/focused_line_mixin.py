# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/focused_line_mixin.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from pikos._internal.function_set import FunctionSet
from pikos._internal.attach_decorators import advanced_attach


class FocusedLineMixin(object):
    """ Mixing class to support recording python line events `focused` on a set
    of functions.

    The method is used along a line event based monitor. It mainly
    overrides the `on_line_event` method to only record events when the
    interpreter is working inside the predefined functions.

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
        # FIXME: There should be a better way to do this
        functions = keywords.pop('functions', ())
        super(FocusedLineMixin, self).__init__(*arguments, **keywords)
        self.functions = FunctionSet(functions)
        self._code_trackers = {}

    def on_line_event(self, frame, why, arg):
        """ Record the line event if we are inside the functions.

        """
        code = frame.f_code
        if code in self.functions:
            event_method = super(FocusedLineMixin, self).on_line_event
            event_method(frame, why, arg)
        return self.on_line_event

    # Override the default attach method to support arguments.
    attach = advanced_attach
