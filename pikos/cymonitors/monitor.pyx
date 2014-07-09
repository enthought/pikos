# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: cymonitors/cmonitor.pyx
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#----------------------------------------------------------------------------
from pikos._internal.attach_decorators import basic_attach
from pikos.monitors.monitor import Monitor as PyMonitor


cdef class Monitor:

    def enable(self):
        pass

    def disable(self):
        pass

    def __enter__(self):
        self.enable()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disable()

    # Use a basic attach decorator.
    attach = basic_attach


PyMonitor.register(Monitor)
