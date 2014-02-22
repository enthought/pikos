# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: cmonitors/pytrace.pxd
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#----------------------------------------------------------------------------
from cpython.pystate cimport (
    Py_tracefunc, PyTrace_CALL, PyTrace_EXCEPTION, PyTrace_LINE,
    PyTrace_RETURN, PyTrace_C_CALL, PyTrace_C_EXCEPTION, PyTrace_C_RETURN,
    PyThreadState)


cdef extern from "frameobject.h":

    ctypedef struct PyFrameObject:
        pass

cdef extern from "Python.h":

    cdef void PyEval_SetProfile(Py_tracefunc func, object arg)
    cdef void PyEval_SetTrace(Py_tracefunc func, object arg)
