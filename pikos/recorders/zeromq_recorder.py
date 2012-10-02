# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: recorders/zeromq_recorder.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import cPickle as pickle
import os

import zmq

from pikos.recorders.abstract_recorder import AbstractRecorder


class RecordingStopped(object):
    pass


class ZeroMQRecorder(AbstractRecorder):
    """ The ZeroMQ Recorder is a recorder that publishes each set of
    values on a 0MQ publish socket.

    Private
    -------
    _filter : callable
        Used to check if the set `record` should be `recored`. The function
        accepts a tuple of the `record` values and return True is the input
        sould be recored.

    _ready : bool
        Singify that the Recorder is ready to accept data. Please use the
        Recorder.ready property

    """

    def __init__(self, zmq_host='127.0.0.1', zmq_port=9001, filter_=None,
                 wait_for_ready=True, **kwargs):
        """ Class initialization.

        Parameters
        ----------
        filter_ : callable
            A callable function that accepts a data tuple and returns True
            if the input sould be recorded.

        """
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PUB)
        self._socket.bind('tcp://{0}:{1}'.format(zmq_host, zmq_port))
        if wait_for_ready:
            self._prepare_socket = self._context.socket(zmq.REQ)
            self._prepare_socket.connect('tcp://{0}:{1}'.format(
                    zmq_host, zmq_port + 1))
        else:
            self._prepare_socket = None
        self._filter = (lambda x: True) if filter_ is None else filter_
        self._ready = not wait_for_ready

    def prepare(self, record):
        """ Write the header in the csv file the first time it is called. """
        if not self._ready:
            ready = False
            handshake_message = pickle.dumps(
                (os.getpid(), "Memory", record._fields))
            while not ready:
                self._prepare_socket.send(handshake_message)
                ready = pickle.loads(self._prepare_socket.recv()) is True
            self._ready = True
            self._prepare_socket.close()
            self._prepare_socket = None

    def finalize(self):
        """ Signal that recording has ended.
        """
        if self._ready:
            self._socket.send(pickle.dumps(RecordingStopped()))

    @property
    def ready(self):
        """ Is the recorder ready to accept data? """
        return self._ready

    def record(self, record):
        """ Rerord entry onlty when the filter function returns True. """
        if self._ready and self._filter(record):
            message = (os.getpid(), record)
            self._socket.send(pickle.dumps(message))
