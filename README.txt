Pikos
=====

Pikos is a profiling and investigation tool suite for python
applications. The name is inspired by Pikos Apikos the main character
in a mid 80s Greek puppet TV series. Pikos was an investigative journalist 
that was assigned to find out about a missing person in the remote
and strange land of of Froutopia, a country populated by fruits that
can talk.

Key aims of Pikos are:

    - Help identify areas of the an application that need to improve.
    - Use, group and augment rather than replace commonly used tools like
      cProfile and line_profiler
    - Provide effective memory monitoring throughout python.
    - Be multi-platform.
    - Provide real-time access to profile data and allow live analysis
      of this while the application is running.

Repository
----------

.. todo:: Add repository info


Installation
------------

The package requires a recent version of psutil (>=0.4.1)::

    python setup.py install

To build with the real-time fork of cProfile, you will need a build of
libzmq to compile and link against. Specify the path to the include
directory (containing ``zmq.h``) and the path to the library file with
which to link::

    python setup.py install --include /path/to/include --zmq-path /path/to/libzmq.so

The installation assumes that the libzqm library will be accessible
from within Python (i.e. you already have pyzmq installed).

Optional packages of external profilers:

- yappi (>=0.62),  `<http://code.google.com/p/yappi/>`_
- line_profiler (>=1.0b3),  `<http://pypi.python.org/pypi/line_profiler>`_

Optional packages for the live monitoring tools:

- pyzmq (>= 2.1.11) `<http://www.zeromq.org/bindings:python>`_
- traits (>= 4.1.0) `<https://github.com/enthought/traits>`_
- traitsui (>= 4.1.0) `<https://github.com/enthought/traitsui>`_
- pyface (>= 4.1.0 `<https://github.com/enthought/pyface>`_
- envisage (>= 4.1.0 `<https://github.com/enthought/envisage>`_
- chaco (>= 4.1.0) `<https://github.com/enthought/chaco>`_
- numpy (>= 1.6.1) `<http://numpy.scipy.org>`_
