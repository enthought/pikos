# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  file: external/yappi_profiler.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from __future__ import absolute_import

import yappi


class YappiProfiler(object):
    """ A pikos compatible profiler class using the yappi library.

    Private
    -------
    _buildins : bool
        Boolean to enable.disable profiling of the buildins.

    The class partially supports the ``Monitor`` decorator for functions (not
    generators) but does not support recorders.


    Notes
    -----
    The class mirrors the module interface. Please refer to the online
    documentation of the yappi module for information and usage of the
    interface (`<http://code.google.com/p/yappi/>`_).

    """

    def __init__(self, recorder=None, builtins=False):
        """ Initialize the profiler class.

        Parameters
        ----------
        builtins : bool
            When set python builtins are also profiled.

        """
        self._builtins = builtins

    def __enter__(self):
        """ Start the yappi profiler if it is not running.
        """
        if  not yappi.is_running():
            yappi.start(self._builtins)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Stop the yappi profiler if it is running.
        """
        if yappi.is_running:
            yappi.stop()

    def start(self, builtins=None):
        builtins = self.builtins if builtins is None else builtins
        yappi.start(builtins)

    def stop(self):
        yappi.stop()

    def enum_stats(self, fenum):
        return yappi.enum_stats(fenum)

    def enum_thread_stats(self):
        return yappi.enum_thread_stats()

    def get_stats(self, *args, **kwrds):
        return yappi.get_stats(*args, **kwrds)

    def print_stats(self, *args, **kwrds):
        yappi.print_stats(*args, **kwrds)

    def clear_stats(self):
        yappi.clear_stats()

    def is_running(self):
        return yappi.is_running()

    def clock_type(self):
        return yappi.clock_type()
