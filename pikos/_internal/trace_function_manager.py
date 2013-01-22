# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  file: _internal/trace_function_manager.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import sys
try:
    import threading
    has_threading = True
except ImportError:
    has_threading = False


class TraceFunctionManager(object):
    """ A Class to replace and recover the functions in sys.settrace.

    ..note:: It can only handle a single replace/recover pair at a time.

    """
    def replace(self, function):
        """ Set a new function in sys.settrace.

        If the function has been already set and it is not the same as before
        then RuntimeError is raised.

        """
        if hasattr(self, 'previous'):
            if function != sys.gettrace():
                raise RuntimeError('Cannot replace profile function more than '
                                   'once')
            return
        else:
            self.previous = sys.gettrace()
        if has_threading:
            threading.settrace(function)
        sys.settrace(function)

    def recover(self):
        """ Unset the current function in the sys.settrace.

        If available the previous method is recovered in settrace. A
        RuntimeError is raised if the `previous` attribute does not exist.

        """
        if hasattr(self, 'previous'):
            sys.settrace(self.previous)
            if has_threading:
                threading.settrace(self.previous)
            del self.previous
        else:
            raise RuntimeError('A profile function has not been set')
