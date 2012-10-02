# Run this with
# ``python -m pikos.monitors.cProfile_rt examples/cprofile_rt.py``

import time
import random
import numpy as np


def main():
    for i in xrange(10):
        arr = np.zeros((1000, 1000))
        time.sleep(random.random())


if __name__ == '__main__':
    main()
