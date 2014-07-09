# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: _internal/attach_decorator.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from pikos._internal.focused_monitor_attach import FocusedMonitorAttach
from pikos._internal.monitor_attach import MonitorAttach


def basic_attach(instance, function):
    """ Attach (i.e. wrap) the monitor to the decorated function.

    Basic decoration functionality without any arguments.

    Parameters
    ----------
    instance : object
        The monitor instance to attach.

    function : callable
        The function to wrap

    Returns
    -------
     fn : callable
        A MonitorAttach instance.

    """
    monitor_attach = MonitorAttach(instance)
    return monitor_attach(function)


def advanced_attach(instance, *args, **kwards):
    """ Attach (i.e. wrap) the monitor to the decorated function.

    This method supports decorating functions with and without keyword
    arguments.

    Parameters
    ----------
    instance : object
        The monitor instance to attach.

    *args : list
        The list of arguments passed to the decorator.

    **kwargs : dict
        The dictionary of keyword arguments passed to the decorator.

    Returns
    -------
    fn : callable
        Depending on the usage of the decorator (with or without
        arguments). The return callable is an instance of:
        - MonitorAttach, if the decorator is used without arguments.
        - FocusedMonitorAttach, if the decorator is used with arguments.

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
        monitor_attach = MonitorAttach(instance)
        return monitor_attach(args[0])
    elif not args:
        monitor_attach = FocusedMonitorAttach(instance, **kwards)
        return monitor_attach
