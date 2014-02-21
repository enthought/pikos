Pikos
=====

Pikos is a profiling and investigation tool suite for python
applications. The name is inspired by Pikos Apikos the main character
in a mid 80s Greek puppet TV series. Pikos was an investigative journalist 
assigned to find out about a missing person case in the remote and strange
land of "Froutopia", a country populated by large fruits that can talk.

Key aims of Pikos are:

    - Help identify areas of the an application that need to improve.
    - Use, group and augment rather than replace commonly used tools like
      cProfile and line_profiler
    - Provide effective memory monitoring throughout python.
    - Be multi-platform.
    - Provide real-time access to profile data and allow live analysis
      while the application is running.

Repository
----------

Pikos is hosted on github: https://github.com/enthought/pikos


Installation
------------

The package requires a recent version of psutil (>=0.4.1)::

    python setup.py install

To build with the real-time fork of cProfile please provide the
`--with-real-time-lsprof` before any setup command::

    python setup.py --with-real-time-lsprof install

You will need a build of libzmq to compile and link against. If the needed files
are not available at system default locations, they will need to be manually 
provided to the ``build_ext`` command::

    python setup.py --with-real-time-lsprof build_ext -I <include directory for zmq> -L <libary directory for zmq>
    python setup.py --with-real-time-lsprof install

or in one line as::

    python setup.py --with-real-time-lsprof build_ext -I <include directory for zmq> -L <library directory for zmq> install

Finally to run the test suite please give::

    python setup.py test

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
