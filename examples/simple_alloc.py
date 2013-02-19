import numpy as np

from pikos.api import memory_on_functions

class Leaky(object):

    def __init__(self, number, shape):
        self.number = number
        self.shape = shape

    def _allocate(self):
        return np.random.rand(*self.shape)

    def allocate(self):
        a = self._allocate()
        b = self._allocate()
        return np.where(a <= 0.25, a, b)

    @memory_on_functions()
    def run(self):
        for i in xrange(self.number):
            self.allocate()

if __name__ == '__main__':
    leaky = Leaky(1, (10000, 10000))
    leaky.run()
