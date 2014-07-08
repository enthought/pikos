# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: _internal/monitor_attach.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import functools
import inspect

from pikos._internal.util import is_context_manager


class MonitorAttach(object):
    """ The monitor attach decorator.


    The class can be instantiated by the user or used as a decorator for
    functions, methods and generators.

    Usage
    -----

    # as a decorator
    @Monitor(FunctionMonitor())
    def my_function():
        ...
        return

    # as an instance
    def my_function():
        ...
        return

    logfunctions = Monitor(FunctionMonitor())
    logfunctions(my_function, *args, **kwrgs)
    ...


    .. tip::

        Alternative easy to use decorators are provided in :mod:`pikos.api`.

    """
    def __init__(self, obj):
        """ Class initialization.

        Parameters
        ----------
        obj : object
            A context manager to monitor instance, inspect or profile the
            decorated
            function while it is executed.
        """
        self._monitor_object = obj

    def __call__(self, function):
        """ Wrap function for monitoring.

        Parameters
        ----------
        function : callable
            The callable to wrap

        Returns
        -------
        fn : callable
            The wrapped function. `fn` has the same signature as `function`.
            Executing `fn` will run `function` inside the
            :attr:`_monitor_object` context.

        Raises
        ------
        ValueError :
            Raised if the provided :attr:`_monitor_object` does not support the
            context manager interface.

        """
        if is_context_manager(self._monitor_object):
            return self._wrap(function)
        else:
            msg = "provided monitor object '{}' is not a context manager"
            ValueError(msg.format(self._monitor_object))

    def _wrap(self, function):
        """ Wrap the callable.

        Returns
        -------
        fn : callable
            The wrapped function. `fn` has the same signature as
            `function`. Special care it taken if the callable is a
            generator.

        """
        if inspect.isgeneratorfunction(function):
            fn = self._wrap_generator(function)
        else:
            fn = self._wrap_function(function)
        return fn

    def _wrap_function(self, function):
        """ Wrap a normal callable object.
        """
        @functools.wraps(function)
        def wrapper(*args, **kwds):
            with self._monitor_object:
                return function(*args, **kwds)
        return wrapper

    def _wrap_generator(self, function):
        """ Wrap a generator function.
        """
        def wrapper(*args, **kwds):
            with self._monitor_object:
                g = function(*args, **kwds)
                value = g.next()
            yield value
            while True:
                with self._monitor_object:
                    item = g.send(value)
                value = (yield item)
        return wrapper
