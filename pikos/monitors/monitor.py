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

from pikos.monitors.attach_decorators import basic_attach


class Monitor(object):
    """ Base class of Pikos provides monitors.

    The class provides the `.attach` decorating method to attach a pikos
    monitor to a function or method. Subclasses might need to provide their
    own implementation if required.

    """
    __metaclass__ = abc.ABCMeta

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

    # Use a basic attach decorator.
    attach = basic_attach