# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: benchmark/record_counter.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from pikos.recorders.abstract_recorder import AbstractRecorder

class RecordCounter(AbstractRecorder):

    def __init__(self):
        self.records = 0

    def prepare(self, record):
        pass

    def finalize(self):
        pass

    def record(self, data):
        self.records += 1
