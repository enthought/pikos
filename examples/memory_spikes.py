""" This example replicates the behaviour of legacy code that creates
data in arrays and then convert them into matrices in order to use in linear
algebra algorithms.

Imagine this implementation hidden inside 10k > lines of code with very
little documentation. Using a function memory monitor you can map the
behaviour of the code and spot possible memory issues before they become
severe. Because narrow peaks will always appear when temporary data are
created even when there is no apparent memory error.

.. note::

    Narrow peeks are the best place to look for correcting possible
    memory issues in the usage of libraries such as numpy, scipy and
    matplotlib.

"""
import argparse
import threading

import numpy as np

from pikos.api import screen, memory_on_functions, monitor_functions
from pikos.cmonitors.cfunction_monitor import CFunctionMonitor


monitor = CFunctionMonitor(recorder=screen())

@monitor.attach
#@monitor_functions(recorder=screen())
def legacy(size):
    b = np.mat(np.random.random(size).T)
    # very bad example that makes copies of numpy arrays when converting them
    # to matrix
    final = None
    def multiply(a, b):
        final = a * b
    a = np.matrix(np.random.random(size))
    t  = threading.Thread(target=multiply, args=(a, b))
    t.start()
    t.join()
    return final.I


@memory_on_functions()
def fixed(size):
    # more appropriate way using a numpy.mat
    b = np.mat(np.random.random(size).T)
    a = np.mat(np.random.random(size))
    final = a * b
    return final.I


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--small',
        action="store_true",
        help='Use a smaller size for the data matrix '
             '(default -- use large size).')
    parser.add_argument(
        '--fixed',
        action="store_true",
        help='Run the corrected code (default -- run the faulty code).')
    args = parser.parse_args()

    if args.small:
        size = (1000, 5000)
    else:
        size = (1000, 20000)

    if args.fixed:
        fixed(size)
    else:
        legacy(size)
