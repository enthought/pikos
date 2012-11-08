# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  file: _internal/profile_function_manager.py
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


class ProfileFunctionManager(object):
    """ A Class to replace and recover the functions in sys.setprofile.

    ..note:: It can only handle a single replace/recover pair at a time.

    """
    def replace(self, function):
        """ Set a new function in sys.setprofile.

        If the function has been already set and it is not the same as before
        then RuntimeError is raised.

        """
        if hasattr(self, 'previous'):
            if function != sys.getprofile():
                raise RuntimeError('Cannot replace profile function more than '
                                   'once')
            return
        else:
            self.previous = sys.getprofile()
        if has_threading:
            threading.setprofile(function)
        sys.setprofile(function)

    def recover(self):
        """ Unset the current function in the sys.setprofile.

        If available the previous method is recovered in setprofile. A
        RuntimeError is raised if the `previous` attribute does not exist.

        """
        if hasattr(self, 'previous'):
            sys.setprofile(self.previous)
            if has_threading:
                threading.setprofile(self.previous)
            del self.previous
        else:
            raise RuntimeError('A profile function has not been set')
