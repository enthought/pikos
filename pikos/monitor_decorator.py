# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import inspect
import functools

from pikos._internal.util import is_context_manager

class MonitorDecorator(object):
    """ The monitor class decorator.

    This is the main entry point for all the monitors, inspectors, loggers and
    profilers that are supported by pikos. The :class:`MonitorDecorator` is simplifies
    setting up and invoking the actual monitoring/profiling class.


    Private
    -------
    _function : callable
        The callable to execute inside the monitor context manager. It can be a
        normal callable object or a generator.

    _monitor_object : object
        The monitor object that implements the context manager interface.


    The class can be instanciated by the user or used as a decorator for
    functions, methods and generators.

    Usage
    -----

    # as a decorator
    @MonitorDecorator(FunctionMonitor())
    def my_function():
        ...
        return

    # as an instance
    def my_function():
        ...
        return

    logfunctions = MonitorDecorator(FunctionMonitor())
    logfunctions(my_function, *args, **kwrgs)
    ...


    .. tip::

        Easy to use decorators are provided in :mod:`pikos.api`.

    """
    def __init__(self, obj):
        """ Class initialization.

        Parameters
        ----------
        obj : object
            A contect manager to monitor, inspect or profile the decorated
            function while it is executed.

        """
        self._function = None
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
        self._function = function
        if is_context_manager(self._monitor_object):
            return self._wrap()
        else:
            msg = "provided monitor object '{}' is not a context manager"
            ValueError(msg.format(self._monitor_object))

    def _wrap(self):
        """ Wrap the callable.

        Returns
        -------
        fn : callable
            The wrapped function. `fn` has the same signature as
            `function`. Special care it taken if the callable is a
            generator.

        """
        if inspect.isgeneratorfunction(self._function):
            fn = self._wrap_generator()
        else:
            fn = self._wrap_function()
        return fn

    def _wrap_function(self):
        """ Wrap a normal callable object.
        """
        @functools.wraps(self._function)
        def wrapper(*args, **kwds):
            with self._monitor_object:
                 return self._function(*args, **kwds)
        return wrapper

    def _wrap_generator(self):
        """ Wrap a generator function.
        """
        def wrapper(*args, **kwds):
            with self._monitor_object:
                g = self._function(*args, **kwds)
                value = g.next()
            yield value
            while True:
                with self._monitor_object:
                    item = g.send(value)
                value = (yield item)
        return wrapper
