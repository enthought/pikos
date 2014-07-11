# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: apikos/task.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#----------------------------------------------------------------------------
from pyface.tasks.action.api import SMenu, SMenuBar
from pyface.tasks.api import Task, EditorAreaPane

from pikos.apikos.constants import APIKOS_TASK


class ApikosTask(Task):

    id = APIKOS_TASK
    name = 'Pikos'

    def _menu_bar_default(self):
        return SMenuBar(SMenu(id='File', name='&File'))

    def create_central_pane(self):
        return EditorAreaPane(task=self)
