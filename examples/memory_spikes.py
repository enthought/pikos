""" This example replicates the behaviour of legacy code that creates
data in arrays and then convert them into matrices in order to use in linear
algebra algorithms.

Imagine this implementation hidden inside 10k > lines of code with very
little documentation. Using a function memory monitor you can map the
behaviour of the code and spot possible memory issues before they become
severe. Because narrow peaks will always appear when temporary data are
created even when there is no apparent memory error.

.. note:: Narrow peeks are the best place to look for correcting possible
    memory issues in the usage of libraries such as numpy, scipy and
    matplotlib.

"""

import numpy as np
from pikos.api import monitor
from pikos.monitors.function_memory_monitor import FunctionMemoryMonitor
from pikos.recorders.zeromq_recorder import ZeroMQRecorder

memory = FunctionMemoryMonitor(ZeroMQRecorder())


@monitor(memory)
def legacy(size):
    b = np.mat(np.random.random(size).T)
    # very bad example that makes copies of numpy arrays when converting them
    # to matrix
    a = np.matrix(np.random.random(size))
    final = a * b
    return final.I


@monitor(memory)
def fixed(size):
    # more approprate way using a numpy.mat
    b = np.mat(np.random.random(size).T)
    a = np.mat(np.random.random(size))
    final = a * b
    return final.I


def simple_loop():
    for i in range(5):
        time.sleep(0.05)

if __name__ == '__main__':
    import sys
    import time

    if '--help' in sys.argv[1:]:
        print \
"""
--small : Use a smaller size for the data matrix (default -- use large size).
--fixed : Run the corrected code (default -- run the faulty code).
"""
        exit()

    if '--small' in sys.argv[1:]:
        size = (1000, 5000)
    else:
        size = (1000, 20000)

    if '--fixed' in sys.argv[1:]:
        fixed(size)
    else:
        legacy(size)

    simple_loop()
