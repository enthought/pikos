# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/monitor_attach.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from pikos.monitors.monitor_attach import MonitorAttach


class FocusedMonitorAttach(MonitorAttach):
    """ The monitor attach decorator for focused monitors.

    This class provides the option for the decorated function to be added in
    the set of functions where the monitor will focus.

    """
    def __init__(self, obj,  include_decorated=False):
        """ Class initialization.

        Parameters
        ----------
        obj : object
            A contect manager to monitor, inspect or profile the decorated
            function while it is executed.

        include_decorated : boolean
            If the decorated function should be included into the list of
            focused functions. Default is False.

        """
        super(FocusedMonitorAttach, self).__init__(obj)
        self._include_decorated = include_decorated

    def _wrap_function(self, function):
        """ Wrap a normal callable object.
        """
        if self._include_decorated:
            self._add_function(function)
        return super(FocusedMonitorAttach, self)._wrap_function(function)

    def _wrap_generator(self, function):
        """ Wrap a generator function.
        """
        if self._include_decorated:
            self._add_function(function)
        return super(FocusedMonitorAttach, self)._wrap_generator(function)

    def _add_function(self, function):
        functions = self._monitor_object.functions
        functions.add(function)
