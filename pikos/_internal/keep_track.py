# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: _internal/keep_track.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
# utility dictionaries for the KeepTrack class
_MODES = {'ping': 1, 'pong': -1}
_CHECKS = {'ping': 1, 'pong': 0}


class KeepTrack(object):
    """ A simple object to keep track of start and stop calls

    The object is used to decide if a initialization or destroy operation needs
    to be performed when a context manager is called recursively.

    usage:
        - Calling the instance with ``ping`` will increase the
          internal counter and return true only the first time it is called.
        - Calling the instance with ``pong`` will decrease the
          internal counter and return False until the counter is zero which
          will pair with the first time the instance was called.

    """
    def __init__(self):
        self._counter = 0

    def __call__(self, mode='ping'):
        """

        Parameters
        ----------
        mode : string
            mode is a String with value 'ping' or 'pong' to indicate the
            operation that is performed in the internal counter.

        Returns
        -------
        A boolean value indicating that an actual *ping* or *pong* needs
        to be performed.

        Note
        ----
        Performing a 'pong' without a corresponding 'ping' will return false.

        """
        self._counter += _MODES[mode]
        if self._counter < 0:
            self._counter = 0
            return False
        else:
            return self._counter == _CHECKS[mode]

    def __nonzero__(self):
        return self._counter > 0
