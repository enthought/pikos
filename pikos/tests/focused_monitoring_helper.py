# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: tests/focused_monitoring_helper.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------

class FocusedMonitoringHelper(object):
    """ A monitoring utility class to help testing 'focused' event monitors.

    """
    @property
    def monitor(self):
        """ The monitor instance that was recently active. """
        return self._monitor
    
    
    def __init__(self, monitor_factory):
        #: The factory accepting a list of  functions that returns 
        #: an monitor instance to use.
        self.monitor_factory = monitor_factory
        #: The python filename where this class is defined
        self.filename = __file__.replace('.pyc', '.py')
        self._monitor = None

    def run_on_function(self):
        """ Run a function under the monitor using the `attach` decorator.

        """
        def gcd(x, y):
            while x > 0:
                x, y = internal(x, y)
            return y

        monitor = self._monitor = self.monitor_factory([gcd])

        def internal(x, y):
            boo()
            return y % x, x

        def boo():
            pass

        @monitor.attach
        def container(x, y):
            boo()
            result = gcd(x, y)
            boo()
            return result

        boo()
        return container(12, 3)


    def run_on_functions(self):
        """ Run functions under the monitor using the `attach` decorator.

        """

        def gcd(x, y):
            while x > 0:
                x, y = internal(x, y)
            return y

        def internal(x, y):
            return y % x, x

        def boo():
            pass

        def foo():
            boo()
            boo()

        monitor = self._monitor = self.monitor_factory([gcd, foo])

        @monitor.attach
        def container(x, y):
            boo()
            result = gcd(x, y)
            boo()
            foo()
            return result

        boo()
        result = container(12, 3)
        boo()
        return result


    def run_on_recursive_function(self):
        """ Run a recursive function under the monitor decorator.

        """
        def gcd(x, y):
            foo()
            return x if y == 0 else gcd(y, (x % y))

        def boo():
            pass

        def foo():
            pass

        monitor = self._monitor = self.monitor_factory([gcd])

        @monitor.attach
        def container(x, y):
            boo()
            result = gcd(x, y)
            boo()
            foo()
            return result

        boo()
        result = container(12, 3)
        boo()
        return result

    def run_on_decorated(self):
        
        def gcd(x, y):
            while x > 0:
                x, y = internal(x, y)
            return y

        def internal(x, y):
            boo()
            return y % x, x

        def boo():
            pass

        monitor = self._monitor = self.monitor_factory([gcd])

        @monitor.attach(include_decorated=True)
        def container(x, y):
            result = gcd(x, y)
            boo()
            return result

        boo()
        result = container(12, 3)
        boo()
        return result


    def run_on_decorated_recursive(self):
        """ Run a recursive function under a focus monitoring the decorated.

        """
        def foo():
            pass

        monitor = self._monitor = self.monitor_factory()

        @monitor.attach(include_decorated=True)
        def gcd(x, y):
            foo()
            return x if y == 0 else gcd(y, (x % y))

        return gcd(12, 3)

