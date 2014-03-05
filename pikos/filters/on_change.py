# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: filters/on_change.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------


class OnChange(object):
    """ A record filter that checks if the record field has changed.

    A copy of the field value is stored in the object and compared against new
    values. On value changed the object returns True.

    Attributes
    ----------
    field : str
        The field to check for change.

    previous :
        Holds the value of the field.

    Notes
    -----
    - Filters and recorders can be shared between monitors. The filter however
      is not aware of ownership so use with care when shareing the same
      instance.
    - This filter only works with nametuple like records.

    """
    def __init__(self, field):
        """ Initialize the filter class.

        Parameters
        ----------
        field : str
            The field to check for change
        """
        self.field = field
        self.previous = None

    def __call__(self, record):
        """ Check if the field in the new record has changed.
        """
        new = getattr(record, self.field)
        check = self.previous != new
        self.previous = new
        return check
