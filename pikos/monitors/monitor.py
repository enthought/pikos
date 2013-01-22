# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: monitors/monitor.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from pikos.monitors.monitor_attach import MonitorAttach


class Monitor(object):
    """ Base class of Pikos provides monitors.

    The class provides the `.attach' decorating method to attach a pikos
    monitor to a function or method. Subclasses might need to provide their
    own implementation if required.

    """
    def attach(self, function):
        monitor_attach = MonitorAttach(self)
        return monitor_attach(function)
