# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: recorders/list_recorder.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import csv

from pikos.recorders.abstract_recorder import AbstractRecorder


class ListRecorder(AbstractRecorder):
    """ The  ListRecorder is simple recorder that records the
    tuple of values in memory as a list.

    Public
    ------
    records : list
        List of records. The Recorder assumes that the record method is
        provided with a tuple and accumulates all the records in a list.

    Private
    -------
    _filter : callable
        Used to check if the data entry should be recorded. The function
        accepts a namedtuple record and return True is the input sould be
        recored.

    """

    def __init__(self, filter_=None):
        """ Class initialization.

        Parameters
        ----------

        filter_ : callable
            A callable function to filter out the data entries that are going
            to be recorded.

        """
        self._filter = (lambda x: True) if filter_ is None else filter_
        self.records = []

    def prepare(self, data):
        """ Prepare the recorder to accept data.

        .. note:: nothing to do for the ListRecorder.

        """
        pass

    def finalize(self):
        """ Finalize the recorder.

        .. note:: nothing to do for the ListRecorder.

        """
        pass

    @property
    def ready(self):
        """ Is the recorder ready to accept data? """
        return True

    def record(self, data):
        """ Rerord the data entry when the filter function returns True.

        Parameters
        ----------
        data : NamedTuple
            The record entry.

        """
        if self.ready and self._filter(data):
            self.records.append(data)
