Usage
=====

The main component in the pikos toolset is the `Monitor`. A monitor creates
a number of records during the execution of the code which are passed on the
recorder to be stored into memory or file.


In code
-------

Monitors can be used programmatically in a number of ways.


#. Enabled/Disabled using the corresponding functions::

    from pikos.api import screen
    from pikos.monitors.api import FunctionMonitor

    monitor = Monitor(recorder=screen())
    monitor.enable()

    # monitored code
    #

    monitor.disable()


#. A monitor instance can be used as a context manager::

    from pikos.api import screen
    from pikos.monitors.api import FunctionMonitor

    monitor = Monitor(recorder=screen())

    with monitor:
        # monitored code
        #
        pass



#. With the use of the `attach` method a monitor becomes a decorator::

    from pikos.api import screen
    from pikos.monitors.api import FunctionMonitor

    monitor = Monitor(recorder=screen())

    @monitor.attach
    def monitored_function():
        # monitored code
        #
        pass


#. Finally the :mod:`pikos.api` module provides easy to use decorator
   factories for the standard monitors that are provided by pikos. The
   factories can optionally accept a recorder and dictate if a focused
   monitor should be used::

    from pikos.api import function_monitor, csv_file

    @function_monitor(recorder=csv_file(), focused=True)
    def monitored_function():
        # monitored code
        #
        pass


Command line
------------

