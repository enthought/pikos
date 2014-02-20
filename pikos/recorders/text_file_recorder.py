# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: recorders/text_stream_recorder.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from pikos.recorders.text_stream_recorder import TextStreamRecorder


class TextFileRecorder(TextStreamRecorder):
    """ The TextStreamRecorder that creates the file for the records.

    Private
    -------
    _stream : TextIOBase
        A text stream what supports the TextIOBase interface. The Recorder
        will write the values as a single line.

    _filter : callable
        Used to check if the set `record` should be `recorded`. The function
        accepts a tuple of the `record` values and return True is the input
        should be recorded.

    _template : str
        A string (using the `Format Specification Mini-Language`) to format
        the set of values in a line. It is constructed when the `prepare`
        method is called.

    _auto_flush : bool
        A bool to enable/disable automatic flushing of the string after each
        record process.

    _ready : bool
        Signify that the Recorder is ready to accept data.

    _filename : string
        The name and path of the file to be used for output.

    """
    def __init__(
            self, filename, filter_=None, formatted=False, auto_flush=False):
        """ Class initialization.

        Parameters
        ----------
        filename : string
            The file path to use.

        filter_ : callable
            A callable function that accepts a data tuple and returns True
            if the input sould be recorded. Default is None.

        formatted : Bool
            Use the predefined formatting in the records. Default value is
            false.

        auto_flush : Bool
            When set the stream buffer is always flushed after each record
            process. Default value is False.

        """
        self._filename = filename
        self._filter = (lambda x: True) if filter_ is None else filter_
        self._formatted = formatted
        self._auto_flush = auto_flush
        self._stream = None
        self._ready = False

    def prepare(self, record):
        """ Open the file and write the header.
        """
        if not self._ready:
            self._stream=open(self._filename, 'w')
            super(TextFileRecorder, self).prepare(record)

    def finalize(self):
        """ Finalize the recorder.

        Raises
        ------
        RecorderError :
            Raised if the method is called without the recorder been ready to
            accept data.

        """
        super(TextFileRecorder, self).finalize()
        if not self._stream.closed:
            self._stream.flush()
            self._stream.close()
