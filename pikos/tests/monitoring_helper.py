# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: tests/gcd.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------

class MonitoringHelper(object):
    """ A monitoring utility class to help testing event monitors.

    """
    def __init__(self, monitor=None):
        #: The monitor instance to use.
        self.monitor = monitor
        #: The python filename where this class is defined
        self.filename = __file__.replace('.pyc', '.py')

    def run_on_function(self):
        """ Run a function under the monitor using the `attach` decorator.

        """
        monitor = self.monitor

        @monitor.attach
        def gcd(x, y):
            while x > 0:
                x, y = y % x, x
            return y

        def boo():
            pass

        boo()
        result = gcd(12, 3)
        boo()
        return result

    def run_on_recursive_function(self):
        """ Run a recursive function under the monitor decorator.

        """
        monitor = self.monitor

        @monitor.attach
        def gcd(x, y):
            return x if y == 0 else gcd(y, (x % y))

        def boo():
            return gcd(7, 12)

        return boo()

    def run_on_generator(self):
        """ Run a generator under the monitor decorator.

        """
        monitor = self.monitor

        @monitor.attach
        def fibonacci(items):
            x, y = 0, 1
            for i in range(items):
                yield x
                x, y = y, x + y

        def boo():
            pass

        boo()
        result = [value for value in fibonacci(10)]
        boo()
        return result

    def run_function_with_internal(self):
        """ Run a function under the monitor decorator.

        """
        monitor = self.monitor

        def gcd(x, y):
            while x > 0:
                x, y = internal(x, y)
            return y

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
