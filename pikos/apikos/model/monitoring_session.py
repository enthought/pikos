# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: apikos/model/base
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#----------------------------------------------------------------------------
from traits.api import Dict, HasStrictTraits, Int, List, Property, Str, Type


class MonitoringSession(HasStrictTraits):

    #: Name of the monitoring session.
    name = Str

    #: Records.
    records = List

    #: The type of the records that have been.
    record_type = Type

    #: Numerical fields
    numerical_fields = Property(Dict(Int, Str))

    def _get_numerical_fields(self):
        return