# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: apikos/plugin.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#----------------------------------------------------------------------------
from envisage.api import Plugin
from envisage.ui.tasks.api import TaskFactory
from traits.api import List

from pikos.apikos.tasks.constants import TASKS


class ApikosPlugin(Plugin):
    """ The main plugin of the apikos application.

    """
    # The plugin's unique identifier.
    id = 'apikos.plugin'

    # The plugin's name (suitable for displaying to the user).
    name = 'Pikos Live Profiling'

    # Envisage contributions.
    tasks = List(contributes_to=TASKS)

    def _tasks_default(self):
        from .task import ApikosTask
        return [TaskFactory(factory=ApikosTask)]
