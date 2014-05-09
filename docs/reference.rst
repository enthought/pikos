Library Reference
=================

Pikos is designed in layers.  At the top layer we find the
:class:`~pikos.monitors.monitor.Monitor` a decorator that acts as the entry
point for the `monitors`_ provided by pikos. The next layer is the various
monitors that are responsible to collect information (e.g. memory) during
the execution of the decorated function. The retrieved information is
recorded through the `recorders`_ and controlled with the `filters`_.

Monitor Decorator
-----------------

.. autoclass:: pikos.monitors.monitor.Monitor

    .. automethod:: pikos.monitors.monitor.Monitor.__init__

    .. automethod:: pikos.monitors.monitor.Monitor.__call__


Monitors
--------

A monitor is a context manager object. The class is initialized with a
recorder class. Each instance of a monitor class can be reused, the
``__enter__`` method makes sure that the code that is executed inside
the context will be monitored and that the associated recorder has
been initialized. During the execution of the decorated function The
information is collected into a name tuple and the tuple is forwarded
to recorder that has been associated with the current monitor.

Pikos currently provides the following monitors:

.. autosummary::

    ~pikos.monitors.function_monitor.FunctionMonitor
    ~pikos.monitors.line_monitor.LineMonitor
    ~pikos.monitors.function_memory_monitor.FunctionMemoryMonitor
    ~pikos.monitors.line_memory_monitor.LineMemoryMonitor
    ~pikos.monitors.focused_function_monitor.FocusedFunctionMonitor
    ~pikos.monitors.focused_line_monitor.FocusedLineMonitor
    ~pikos.monitors.focused_function_memory_monitor.FocusedFunctionMemoryMonitor
    ~pikos.monitors.focused_line_memory_monitor.FocusedLineMemoryMonitor

External Monitors
*****************

Pikos can act as entry point for external libraries and profilers.

.. autosummary::

   ~pikos.external.python_cprofiler.PythonCProfiler
   ~pikos.external.line_profiler.LineProfiler
   ~pikos.external.yappi_profiler.YappiProfiler

.. note:: These profilers are experimental and not yet integrated fully
  with the pikos framework. Please check individual documentation for
  more information.

Recorders
---------

The recorder (a subclass of
:class:`~pikos.recorders.abstract_recorder.AbstractRecorder`) is
responsible for recording the tuples from the monitor. What is
recordered is controlled by a filter function

Pikos currently provides the following recorders:

.. autosummary::

    ~pikos.recorders.text_stream_recorder.TextStreamRecorder
    ~pikos.recorders.text_file_recorder.TextFileRecorder
    ~pikos.recorders.csv_recorder.CSVRecorder
    ~pikos.recorders.csv_file_recorder.CSVFileRecorder
    ~pikos.recorders.list_recorder.ListRecorder
    ~pikos.recorders.zeromq_recorder.ZeroMQRecorder

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

    ~pikos.filters.on_value.OnValue
    ~pikos.filters.on_change.OnChange

Records
-------

Each monitor uses a specific record. A record is a subclass of named
tuple augmented with two methods, ``header``, ``line`` that can be
optionally used to format the output.

.. note::

    Currently only the
    :class:`~pikos.recorders.test_stream_recorder.TextStreamRecorder`
    can take advantage of the additional format information.

The monitor records available are:

.. autosummary::

    ~pikos.monitors.records.FunctionRecord
    ~pikos.monitors.records.LineRecord
    ~pikos.monitors.records.FunctionMemoryRecord
    ~pikos.monitors.LineMemoryRecord


----------------------------------

.. toctree::
    :hidden:

    monitors
    recorders
    filters
    external
