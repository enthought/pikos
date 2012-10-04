import sys
import numpy as np
from pikos.api import monitor
from pikos.recorders.text_stream_recorder import TextStreamRecorder
from pikos.monitors.function_memory_monitor import FunctionMemoryMonitor, \
    FunctionMemoryRecordFormater

recorder = TextStreamRecorder(sys.stdout, auto_flush=True,
                              formater=FunctionMemoryRecordFormater())


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
        return a[np.where(a <= 0.25, a, b)]

    @monitor(FunctionMemoryMonitor(recorder))
    def run(self):
        for i in xrange(self.number):
            self.allocate()

if __name__ == '__main__':
    leaky = Leaky(1, (10000, 10000))
    leaky.run()
