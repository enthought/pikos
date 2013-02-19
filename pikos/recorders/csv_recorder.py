# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: recorders/csv_recorder.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import csv

from pikos.recorders.abstract_recorder import AbstractRecorder, RecorderError


class CSVRecorder(AbstractRecorder):
    """ The CSV Recorder is a simple text based recorder that records the
    tuple of values using a scv writer.

    Private
    -------
    _filter : callable
        Used to check if the set `record` should be `recorded`. The function
        accepts a tuple of the `record` values and return True is the input
        sould be recored.

    _writer : csv.writer
        The `writer` object is owned by the CSVRecorder and exports the record
        values according to the configured dialect.

    _ready : bool
        Singify that the Recorder is ready to accept data.

    """

    def __init__(self, stream, filter_=None, **csv_kwargs):
        """ Class initialization.

        Parameters
        ----------
        stream : file
            A *file*-like object to use for output.

        filter_ : callable
            A callable function that accepts a data tuple and returns True
            if the input sould be recorded.

        **csv_kwargs :
            Key word arguments to be passed to the *cvs.writer*.

        """
        self._filter = (lambda x: True) if filter_ is None else filter_
        self._writer = csv.writer(stream, **csv_kwargs)
        self._ready = False

    def prepare(self, fields):
        """ Write the header in the csv file the first time it is called. """
        if not self._ready:
            self._writer.writerow(fields)
            self._ready = True

    def finalize(self):
        """ Finalize the recorder.

        A do nothing method.

        Raises
        ------
        RecorderError :
            Raised if the method is called without the recorder been ready to
            accept data.

        """
        if not self._ready:
            msg = 'Method called while recorder has not been prepared'
            raise RecorderError(msg)

    def record(self, data):
        """ Record the data entry when the filter function returns True.

        Parameters
        ----------
        values : NamedTuple
            The record entry.

        Raises
        ------
        RecorderError :
            Raised if the method is called without the recorder been ready to
            accept data.

        """
        if self._ready:
            if self._filter(data):
                self._writer.writerow(data)
        else:
            msg = 'Method called while recorder is not ready to record'
            raise RecorderError(msg)
