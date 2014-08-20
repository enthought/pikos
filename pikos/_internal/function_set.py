# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: _internal/function_set.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import collections
import inspect
import warnings


class FunctionSet(collections.MutableSet):
    """ A mutable set of functions.

    """

    def __init__(self, functions=None):
        """ Initialize the function container class.

        Parameters
        ----------
        recorder : object
            A subclass of :class:`~pikos.recorders.AbstractRecorder` or a class
            that implements the same interface to handle the values to be
            logged.

        functions : list
            A list of function or method objects inside which recording will
            take place.

        """
        self._code_map = {}
        self.functions = []
        for function in functions:
            self.add(function)

    def __contains__(self, item):
        """ Check it the function set contains the provided code object or
        function.

        """
        if inspect.iscode(item):
            return item in self._code_map
        else:
            return item in self.functions

    def __iter__(self):
        """ Iterate over the function objects.

        """
        return iter(self.functions)

    def __len__(self):
        return len(self.functions)

    def add(self, function):
        """ Add the Python function to the list of monitored functions.

        Parameters
        ----------
        function : object
            A function or method object to add to the list of monitored
            functions. If the function is already included then the method
            exits silently.

        Notes
        -----
        Code adapted from the line_profiler package.

        """
        try:
            code = function.func_code
        except AttributeError:
            if inspect.isbuiltin(function):
                msg = "Built-in functions are not supported for: {0}"
            else:
                msg = "Could not extract a code object for: {0}"
            warnings.warn(msg.format(function))
        else:
            if code not in self._code_map:
                self._code_map[code] = {}
                self.functions.append(function)

    def discard(self, function):
        """ Remove the Python function form the list of monitored functions.

        Parameters
        ----------
        function : object
            The function or method object to remove from the list of monitored
            functions. If the function does not exist in the list then the
            method exists silently.

        """
        try:
            code = function.func_code
        except AttributeError:
            msg = "Could not extract a code object for the object {0}"
            warnings.warn(msg.format(function))
        else:
            if code in self._code_map:
                self._code_map.pop(code)
                self.functions.remove(function)
