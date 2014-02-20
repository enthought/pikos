Usage
=====

The main component in the pikos toolset is the `Monitor`. This item can be
enabled/disabled using the corresponding functions::

    from pikos.api import screen
    from pikos.monitors.api import FunctionMonitor

    monitor = Monitor(recorder=screen())
    monitor.enable()

    # monitored code
    #

    monitor.disable()

Alternative a monitor instance can be used as a context manager::

    from pikos.api import screen
    from pikos.monitors.api import FunctionMonitor

    monitor = Monitor(recorder=screen())
     with monitor:
        # monitored code
        #

Or as a decorator::

    from pikos.api import screen
    from pikos.monitors.api import FunctionMonitor

    monitor = Monitor(recorder=screen())

    @monitor.attach
    def monitored_function():
        # monitored code
        #

Finally the :mod:`pikos.api` module provides easy to use decorators for the
standard monitors provided by pikos::

    from pikos.api import function_monitor, csv_file

    @function_monitor(recorder=csv_file)
    def monitored_function():
        # monitored code
        #








