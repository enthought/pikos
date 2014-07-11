# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: apikos/application.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#----------------------------------------------------------------------------
from envisage.ui.tasks.api import TasksApplication
from pyface.tasks.api import TaskWindowLayout


class ApikosApplication(TasksApplication):

    id = 'apikos.gui'
    name = 'Apikos'

    def _default_layout_default(self):
        tasks = [factory.id for factory in self.task_factories]
        return [TaskWindowLayout(*tasks, size=(1024, 768))]
