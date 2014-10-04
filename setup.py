# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  file: setup.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2011-2014, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import os
import platform

from setuptools import setup, find_packages, Extension, Feature

try:
    from Cython.Distutils import build_ext
except ImportError:
    CAN_BUILD_CYTHON_MONITORS = False
    cmdclass = {}
else:
    CAN_BUILD_CYTHON_MONITORS = platform.python_implementation() == 'CPython'
    cmdclass = {'build_ext': build_ext}

try:
    import unittest2
except ImportError:
    test_suite = 'pikos.tests'
else:
    test_suite = 'unittest2.collector'


with open('README.rst', 'r') as readme:
    README_TEXT = readme.read()


real_time_lsprof = Feature(
    description='optional real time lsrof using zmq',
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

features = {'real-time-lsprof': real_time_lsprof}

cython_monitors = Feature(
    description='optional compile additional cython monitors',
    standard=CAN_BUILD_CYTHON_MONITORS,
    ext_modules=[
        Extension(
            'pikos.cymonitors.monitor',
            sources=['pikos/cymonitors/monitor.pyx']),
        Extension(
            'pikos.cymonitors.function_monitor',
            sources=[
                'pikos/cymonitors/function_monitor.pyx']),
        Extension(
            'pikos.cymonitors.line_monitor',
            sources=[
                'pikos/cymonitors/line_monitor.pyx']),
        Extension(
            'pikos.cymonitors.focused_function_monitor',
            sources=[
                'pikos/cymonitors/focused_function_monitor.pyx']),
        Extension(
            'pikos.cymonitors.focused_line_monitor',
            sources=[
                'pikos/cymonitors/focused_line_monitor.pyx']),
        Extension(
            'pikos.cymonitors.function_memory_monitor',
            sources=[
                'pikos/cymonitors/function_memory_monitor.pyx']),
        Extension(
            'pikos.cymonitors.focused_function_memory_monitor',
            sources=[
                'pikos/cymonitors/focused_function_memory_monitor.pyx']),
        Extension(
            'pikos.cymonitors.line_memory_monitor',
            sources=[
                'pikos/cymonitors/line_memory_monitor.pyx']),
        Extension(
            'pikos.cymonitors.focused_line_memory_monitor',
            sources=[
                'pikos/cymonitors/focused_line_memory_monitor.pyx'])])


features['cython-monitors'] = cython_monitors


VERSION = '0.2.0dev'


def write_version_py(filename=None):
    if filename is None:
        filename = os.path.join(
            os.path.dirname(__file__), 'pikos', 'version.py')
    ver = """\
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  Package: Pikos toolkit
#  File: version.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2012-14, Enthought, Inc.
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
    packages=find_packages(),
    test_suite=test_suite,
    entry_points=dict(
        console_scripts=['pikos-run = pikos.runner:main']),
    cmdclass=cmdclass,
    features=features)
