# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: recorders/text_stream_recorder.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import os

from pikos.recorders.abstract_recorder import AbstractRecorder, RecorderError


class TextStreamRecorder(AbstractRecorder):
    """ The TextStreamRecorder is simple recorder that formats and writes the
    records directly to a stream.

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

    """
    def __init__(self, text_stream, filter_=None, formatted=False,
                 auto_flush=False):
        """ Class initialization.

        Parameters
        ----------
        text_stream : TextIOBase
            A text stream what supports the TextIOBase interface.

        filter_ : callable
            A callable function that accepts a data tuple and returns True
            if the input sould be recorded.

        formatted : Bool
            Use the predefined formatting in the records. Default value is
            false.

        auto_flush : Bool
            When set the stream buffer is always flushed after each record
            process. Default value is False.

        """
        self._filter = (lambda x: True) if filter_ is None else filter_
        self._stream = text_stream
        self._formatted = formatted
        self._auto_flush = auto_flush
        self._ready = False

    def prepare(self, data):
        """ Prepare the recorder to accept data.

        Parameters
        ----------
        data : NamedTuple
            An example data record to prepare the recorder and write the
            header to the stream

        """
        if not self._ready:
            self._writeheader(data)
            self._ready = True

    def finalize(self):
        """ Finalize the recorder

        A do nothing method.

        Raises
        ------
        RecorderError :
            Raised if the method is called without the recorder been ready to
            accept data.

        """
        if not self._ready:
            msg = 'Method called while recorder has not been prepared yet'
            raise RecorderError(msg)

    def record(self, data):
        """ Rerord the data entry when the filter function returns True.

        Parameters
        ----------
        data : NamedTuple
            The record entry.

        Raises
        ------
        RecorderError :
            Raised if the method is called without the recorder been ready to
            accept data.


        Notes
        -----
        Given the value of :attr:`_auto_flush` the recorder will flush the
        stream buffers after each record.

        """
        if self._ready:
            if self._filter(data):
                line = self._format(data)
                self._stream.write(line)
                if self._auto_flush:
                    self._stream.flush()
        else:
            msg = 'Method called while recorder is not ready to record'
            raise RecorderError(msg)

    def _writeheader(self, data):
        """ Write the header to the stream.

        The header is created and sent to the stream followed by the separator
        line. The stream buffers are flushed if necessary.

        Parameters
        ----------
        data : class
            The class of the data entry record.

        """
        if self._formatted:
            header = data.header()
        else:
            header = ' '.join(str(value) for value in data._fields)
            header += os.linesep

        separator = '-' * (len(header) - len(os.linesep)) + os.linesep
        self._stream.write(header)
        self._stream.write(separator)
        if self._auto_flush:
            self._stream.flush()

    def _format(self, data):
        """ Format the data entry to a line.

        Parameters
        ----------
        data : NamedTuple
            The record entry.

        Returns
        -------
        line : str
            The string representation of the data entry.

        """
        if self._formatted:
            line = data.line()
        else:
            line = ' '.join(str(value) for value in data) + os.linesep
        return line
