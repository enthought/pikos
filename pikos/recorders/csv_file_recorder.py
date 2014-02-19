# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: recorders/csv_recorder.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from pikos.recorders.csv_recorder import CSVRecorder


class CSVFileRecorder(CSVRecorder):
    """ A CSVRecorder that creates the stream (i.e. file) for the records.

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

    _filename : string
        The name and path of the file to be used for output.

    _file : file
        The file object where records are stored.

    """

    def __init__(self, filename, filter_=None, **csv_kwargs):
        """ Class initialization.

        Parameters
        ----------
        filename : string
            The file path to use.

        filter_ : callable
            A callable function that accepts a data tuple and returns True
            if the input sould be recorded. Default is None.

        **csv_kwargs :
            Key word arguments to be passed to the *cvs.writer*.

        """
        self._filename = filename
        self._file = open(self._filename, 'wb')
        super(CSVFileRecorder, self).__init__(
            self._file, filter_=filter_, **csv_kwargs)

    def finalize(self):
        """ Finalize the recorder.

        Raises
        ------
        RecorderError :
            Raised if the method is called without the recorder been ready to
            accept data.

        """
        super(CSVFileRecorder, self).finalize()
        if not self._file.closed:
            self._file.flush()
            self._file.close()
