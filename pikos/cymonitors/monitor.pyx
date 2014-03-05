# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: cymonitors/cmonitor.pyx
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#----------------------------------------------------------------------------
from pikos.monitors.monitor_attach import MonitorAttach
from pikos.monitors.monitor import Monitor as PyMonitor


cdef class Monitor:

    def enable(self):
        pass

    def disable(self):
        pass

    def attach(self, function):
        monitor_attach = MonitorAttach(self)
        return monitor_attach(function)

    def __enter__(self):
        self.enable()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disable()


PyMonitor.register(Monitor)
