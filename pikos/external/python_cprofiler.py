# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  file: external/python_cprofiler.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from __future__ import absolute_import
import cProfile

from pikos._internal.keep_track import KeepTrack

class PythonCProfiler(cProfile.Profile):
    """ The normal python :class:`~cProfiler.Profile` subclassed and adapted to
    work with the pikos MonitorDecorator decorator.

    The class fully supports the ``MonitorDecorator`` decorator for functions and
    generators but does not support recorders.

    Notes
    -----
    Due to the function wrapping a small overhead is expected especially if the
    decorated function is recursive calls.  The ``wrapper`` function and the
    ``__enter__`` and ``__exit__`` methods of the context manager might also
    appear in the list of functions that have been called.


    """
    def __init__(self, *args, **kwrds):
        """ Initialize the cProfiler wrapper class.

        Please refer to the pyhton documentation for initialization options.

        """
        super(PythonCProfiler, self).__init__(*args, **kwrds)
        self._call_tracker = KeepTrack()

    def __enter__(self):
        if self._call_tracker('ping'):
            self.enable()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._call_tracker('pong'):
            self.disable()
