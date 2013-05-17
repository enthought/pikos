# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  file: setup.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import os
from setuptools import setup, find_packages, Extension, Feature

with open('README.rst', 'r') as readme:
    README_TEXT = readme.read()


real_time_lsprof = Feature(
    'optional real time lsrof using zmq',
    standard=False,
    ext_modules=[
        Extension(
            'pikos._internal._lsprof_rt',
            sources=['pikos/_internal/_lsprof_rt.c',
                     'pikos/_internal/rotatingtree.c'],
            libraries=['zmq'],
        ),
    ]
)


VERSION = '0.1.0dev1'


def write_version_py(filename=None):
    if filename is None:
        filename = os.path.join(os.path.dirname(__file__),
                                'pikos', 'version.py')
    ver = """\
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: version.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
version = '%s'
"""
    fh = open(filename, 'wb')
    try:
        fh.write(ver % VERSION)
    finally:
        fh.close()


write_version_py()


setup(
    name='pikos',
    version=VERSION,
    author='Enthought Inc',
    author_email='info@enthought.com',
    description='Enthought monitoring and profiling tools',
    long_description=README_TEXT,
    requires=['psutil'],
    install_requires=['distribute'],
    packages=find_packages(),
    test_suite='pikos.tests',
    entry_points=dict(
        console_scripts=['pikos-run = pikos.runner:main']),
    features={'real-time-lsprof': real_time_lsprof})
