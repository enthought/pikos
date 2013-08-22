# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: filters/on_value.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
class NotOnValue(object):
    """ A record filter that removes the record when a value is present.

    Attributes
    ----------
    field : str
        The field to check for change.

    values :
        A list of values to use for the filtering.

    """
    def __init__(self, field, *args):
        """ Initialize the filter class.

        Parameters
        ----------
        field : str
            The field to check for change

        *args :
            A list of values to look for.

        """
        self.field = field
        self.values = list(args)

    def __call__(self, record):
        """ Check for the value in the field.
        """
        value = getattr(record, self.field)
        return value not in self.values
