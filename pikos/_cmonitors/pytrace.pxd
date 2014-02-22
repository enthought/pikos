from cpython.pystate cimport (
    Py_tracefunc, PyTrace_CALL, PyTrace_EXCEPTION, PyTrace_LINE,
    PyTrace_RETURN, PyTrace_C_CALL, PyTrace_C_EXCEPTION, PyTrace_C_RETURN)


cdef extern from "Python.h":

    cdef void PyEval_SetProfile(Py_tracefunc func, object arg)
    cdef void PyEval_SetTrace(Py_tracefunc func, object arg)

TRACETOSTR = {
    PyTrace_CALL:        'call',
    PyTrace_EXCEPTION:   'exc',
    PyTrace_LINE:        'line',
    PyTrace_RETURN:      'return',
    PyTrace_C_CALL:      'c_call',
    PyTrace_C_EXCEPTION: 'c_exc',
    PyTrace_C_RETURN:    'c_ret',
}.get
