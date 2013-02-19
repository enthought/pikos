import os
from random import random

import numpy as np
import psutil

from pikos.external.api import PythonCProfiler


cprofiler = PythonCProfiler()


class Leaker(object):

    def __init__(self, number, shape):
        self.number = number
        self.shape = shape
        self.leaks = []

    def _make_array(self, big=False):
        if big:
            shape = (self.shape[0] * 5, self.shape[1] * 2)
        else:
            shape = self.shape
        return np.empty(shape)

    def _leak(self):
        foo = self._make_array(big=True)
        foo = self._bad_add_to_array(foo, 1.)
        self.leaks.append(foo)

    def _bad_add_to_array(self, array, value):
        return np.array(array) + value

    def _spike(self):
        foo = self._make_array(big=True)
        foo = self._bad_add_to_array(foo, 1.)

    def _dont_leak(self):
        self._make_array()

    @cprofiler.attach
    def run_leaky(self):
        for i in xrange(self.number):
            num = random()
            if num < 0.025:
                self._leak()
            elif num < 0.1:
                self._spike()
            else:
                self._dont_leak()


if __name__ == '__main__':
    proc = psutil.Process(os.getpid())
    leaker = Leaker(100, (1000, 1000))
    leaker.run_leaky()

    cprofiler.print_stats()
