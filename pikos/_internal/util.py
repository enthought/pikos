# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: _internal/util.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------


def is_context_manager(obj):
    """ Check if the obj is a context manager """
    # FIXME: this should work for now.
    return hasattr(obj, '__enter__') and hasattr(obj, '__exit__')


def trim_left(value, max_length):
    """ Trim the left side of the string so that the length is at most
    max_length.

    """
    str_value = str(value)
    return str_value[-max_length:len(str_value)]
