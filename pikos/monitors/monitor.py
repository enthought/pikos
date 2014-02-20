# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import abc

from pikos.monitors.monitor_attach import MonitorAttach


class Monitor(object):
    """ Base class of Pikos provides monitors.

    The class provides the `.attach` decorating method to attach a pikos
    monitor to a function or method. Subclasses might need to provide their
    own implementation if required.

    """
    __metaclass__ = abc.ABCMeta

    def attach(self, function):
        """ Attach (i.e. wrap) the monitor to the function.

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
        monitor_attach = MonitorAttach(self)
        return monitor_attach(function)

    @abc.abstractmethod
    def enable(self):
        """ This method should enable the monitor.
        """

    @abc.abstractmethod
    def disable(self):
        """ This method should disable the monitor.

        """

    def __enter__(self):
        """ The entry point of the context manager.

        Default implementation is calling :meth:`enable`.

        """
        self.enable()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ The exit point of the context manager.

        Default implementation is calling :meth:`disable`.

        """
        self.disable()
