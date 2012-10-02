Library Reference
=================

Pikos is designed in layers.  At the top layer we find the
:class:`~pikos.monitor_decorator.MonitorDecorator` a decorator that acts as an
the entry point for the `monitors`_ provided to wrap methods to be monitored.
The next layer is the various monitors that are responsible to collect
information (e.g. memory) during the execution of the decorated function.
The retrieved information is recorded through the `recorders`_ and controlled
with the `filters`_.

MonitorDecorator Decorator
-----------------

.. autoclass:: pikos.monitor_decorator.MonitorDecorator

    .. automethod:: pikos.monitor_decorator.MonitorDecorator.__init__

    .. automethod:: pikos.monitor_decorator.MonitorDecorator.__call__


Monitors
--------

A monitor is a context manager object. The class is initialized with a
recorder class. Each instance of a monitor class can be reused, the
``__enter__`` method makes sure that the code that is executed insider
the context will be monitored and that the associated recorder has
been initialized. During the execution of the decorated function The
information is collected into a name tuple and the tuple is forwarded
to recorder that has been associated with the current monitor.

Pikos currently provides the following monitors:

.. autosummary::

    pikos.monitors.function_monitor.FunctionMonitor
    pikos.monitors.line_monitor.LineMonitor
    pikos.monitors.function_memory_monitor.FunctionMemoryMonitor
    pikos.monitors.line_memory_monitor.LineMemoryMonitor

External Monitors
*****************

Pikos can act as entry point for external libraries and profilers.

.. autosummary::

   pikos.external.python_cprofiler.PythonCProfiler
   pikos.external.line_profiler.LineProfiler
   pikos.external.yappi_profiler.YappiProfiler

.. note:: These profilers are experimental and not yet integrated fully
  in the pikos framework. Please check individual documentation for
  more information.

Recorders
---------

The recorder (a subclass of
:class:`~pikos.recorders.abstract_recorder.AbstractRecorder`) is
responsible for recording the tuples from the monitor. What is
recordered is controlled by a filter function

Pikos currently provides the following recorders:

.. autosummary::

    pikos.recorders.text_stream_recorder.TextStreamRecorder
    pikos.recorders.csv_recorder.CSVRecorder
    pikos.recorders.list_recorder.ListRecorder
    pikos.recorders.zeromq_recorder.ZeroMQRecorder

.. note:: The standard Recorders are record type agnostic so it is
 possible to use the same recorder for multiple monitors. However,
 this feature is experimental and users are advised to use with care.

Filters
-------

A filter controls if a record tuple will be recorded or not. The
callable accepts the record and makes a decision based on that
(i.e. return ``True`` or ``False``.  Functions (normal and lamda) and
callable classes can be used in this case to remove clutter and speed
up monitoring only of the desired code.

Pikos currently provides the following predefined filters:

.. autosummary::

    pikos.filters.on_value.OnValue
    pikos.filters.on_change.OnChange

Records
-------

Each monitor uses a specific record. A record is a subclass of named
tuple augmented with two methods, ``header``, ``line`` that can
optionally used for formating by the recorders.

.. note::

    Currently only the
    :class:`~pikos.recorders.test_stream_recorder.TextStreamRecorder`
    can take advantage of the additional formating functionality.

The monitor records available are:

.. autosummary::

    pikos.monitors.function_monitor.FunctionRecord
    pikos.monitors.line_monitor.LineRecord
    pikos.monitors.function_memory_monitor.FunctionMemoryRecord
    pikos.monitors.line_memory_monitor.LineMemoryRecord


----------------------------------

.. toctree::
    :hidden:

    monitors
    recorders
    filters
    external
