# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/focused_function_mixin.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from pikos.monitors.focused_monitor_attach import FocusedMonitorAttach
from pikos._internal.function_set import FunctionSet
from pikos._internal.keep_track import KeepTrack


class FocusedMonitorMixin(object):
    """ Base Mixing class for monitors to support decorating functions with
    and without keyword arguments.

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
        super(FocusedMonitorMixin, self).__init__(*arguments, **keywords)
        self.functions = FunctionSet(functions)

    def attach(self, *args, **kwards):
        """ Attach (i.e. wrap) the focused monitor to the decorated function.

        This method supports decorating functions with and without keyword
        arguments.

        Parameters
        ----------
        function : callable
            The callable to wrap

        include_decorated : boolean
            If the decorated function should be included into the list of
            focused functions. Default is False.

        Returns
        -------
        fn : callable
            Depedning on the usage of the decorator (with or without
            arguments). The return callable is

            - The wrapped function, if the decorator is used without arguments.
              `fn` has the same signature as `function`. Executing `fn` will
              run `function` inside the :attr:`_monitor_object` context.

            - A factory for the wrapped function, if the decorator is used with
              arguments. Calling `fn` with the `function` will return the
              decorated function that has the same signature as `function`.
              Executing the decorated function will then run `function` inside
              the :attr:`_monitor_object` context.

        Raises
        ------
        TypeError :
            Raised if the monitor cannot be attached to the function.

        """
        if args and len(kwards) > 0:
            msg = (
                "Cannot attach monitor as a decorator without arguments"
                " when there are keyword arguments provided")
            raise TypeError(msg)
        elif len(args) == 1 and not callable(args[0]):
            msg = (
                "Cannot attach monitor as a decorator without arguments"
                " when a callable to decorate is not provided")
            raise TypeError(msg)
        elif len(args) == 1 and callable(args[0]):
            return super(FocusedMonitorMixin, self).attach(args[0])
        elif not args:
            monitor_attach = FocusedMonitorAttach(self, **kwards)
            return monitor_attach
